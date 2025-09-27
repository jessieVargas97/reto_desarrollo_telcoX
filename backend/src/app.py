from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random
from config import Config
from models import Base, Customer, Consumption

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

api = Api(app, version="1.0", title="TelcoX Mock API", doc="/docs",
          description="API RESTful para visualizar consumo, saldo y minutos.")
ns = api.namespace("api", description="Endpoints de consumo")

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
init_db()

consumption_model = api.model("Consumption", {
    "msisdn": fields.String(required=True),
    "name": fields.String(required=True),
    "balance": fields.Float(required=True),
    "data_mb": fields.Float(required=True),
    "minutes": fields.Integer(required=True),
    "updated_at": fields.DateTime(required=True),
})

consumption_list_model = api.model("ConsumptionList", {
    "results": fields.List(fields.Nested(consumption_model))
})

error_model = api.model("Error", {"message": fields.String})

## Endpoints ##


#Retorna el estado del servicio
@ns.route("/health")
class Health(Resource):
    def get(self):
        return {"status": "ok", "time": datetime.utcnow().isoformat()+"Z"}

#Retorna los datos de los clientes 
@ns.route("/consumption")
class ConsumptionView(Resource):
    @ns.param('msisdn', 'Opcional. Si lo envías retorna ese MSISDN; si no, retorna lista.', _in='query', required=False)
    @ns.response(200, "OK")
    @ns.response(404, "No encontrado", model=error_model)
    @ns.response(500, "Error interno", model=error_model)
    def get(self):
        msisdn = request.args.get("msisdn")
        db = SessionLocal()
        try:
            if msisdn:
                cust = db.execute(select(Customer).where(Customer.msisdn == msisdn)).scalar_one_or_none()
                if not cust:
                    return {"message": "Cliente no encontrado"}, 404
                cons = db.execute(
                    select(Consumption)
                    .where(Consumption.msisdn == msisdn)
                    .order_by(Consumption.updated_at.desc())
                ).scalar_one_or_none()
                if not cons:
                    return {"message": "Consumo no encontrado"}, 404
                return {
                    "msisdn": msisdn,
                    "name": cust.name,
                    "balance": round(cons.balance, 2),
                    "data_mb": round(cons.data_mb, 2),
                    "minutes": int(cons.minutes),
                    "updated_at": cons.updated_at.isoformat()+"Z",
                }, 200

            customers = db.execute(select(Customer)).scalars().all()
            results = []
            for c in customers:
                cons = db.execute(
                    select(Consumption)
                    .where(Consumption.msisdn == c.msisdn)
                    .order_by(Consumption.updated_at.desc())
                ).scalar_one_or_none()
                if cons:
                    results.append({
                        "msisdn": c.msisdn,
                        "name": c.name,
                        "balance": round(cons.balance, 2),
                        "data_mb": round(cons.data_mb, 2),
                        "minutes": int(cons.minutes),
                        "updated_at": cons.updated_at.isoformat()+"Z",
                    })
            return {"results": results}, 200
        except Exception as e:
            return {"message": f"Error interno: {e}"}, 500
        finally:
            db.close()

#Permite realiar una simulacion de actualizacion de datos para ser consultados posteriormente
@ns.route("/consumption/simulate")
class ConsumptionSim(Resource):
    @ns.response(200, "OK")
    def post(self):
        payload = (request.get_json(silent=True) or {})
        msisdn = payload.get("msisdn")
        db = SessionLocal()
        try:
            q = select(Consumption)
            if msisdn:
                q = q.where(Consumption.msisdn == msisdn)
            rows = db.execute(q).scalars().all()
            changed = 0
            for r in rows:
                r.data_mb = max(0.0, r.data_mb - random.uniform(1, 15))
                r.minutes = max(0, r.minutes - random.randint(0, 3))
                r.balance = max(0.0, r.balance - random.uniform(0.01, 0.15))
                r.updated_at = datetime.utcnow()
                changed += 1
            db.commit()
            return {"updated": changed}, 200
        except Exception as e:
            db.rollback()
            return {"message": f"Error: {e}"}, 500
        finally:
            db.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)