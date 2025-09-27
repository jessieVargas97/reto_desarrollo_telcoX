import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
interface Consumption {
  msisdn: string; name: string; balance: number; data_mb: number; minutes: number; updated_at: string;
}
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Panel de Consumo TelcoX';
  msisdn = '593988877766';
  loading = false;
  error: string | null = null;
  data: Consumption | null = null;
  constructor(private http: HttpClient) {}
  fetch() {
    this.loading = true; this.error = null;
    this.http.get<Consumption>(`/api/consumption?msisdn=${this.msisdn}`).subscribe({
      next: (res) => { this.data = res; this.loading = false; },
      error: (err) => { this.error = err?.error?.message || 'Error desconocido'; this.loading = false; }
    });
  }
  simulate() {
    this.http.post(`/api/consumption/simulate`, { msisdn: this.msisdn }).subscribe(() => this.fetch());
  }
  ngOnInit() {
    this.fetch();
    setInterval(() => this.fetch(), 10000);
  }
}