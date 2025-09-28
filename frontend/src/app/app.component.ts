import { Component, OnDestroy, OnInit } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Subscription, interval, switchMap } from 'rxjs';

interface Consumption {
  msisdn: string; name: string; balance: number; data_mb: number; minutes: number; updated_at: string;
}

@Component({ selector: 'app-root', templateUrl: './app.component.html' })
export class AppComponent implements OnInit, OnDestroy {
  title = 'TelcoX';
  msisdn = '';
  list: Consumption[] = [];
  item?: Consumption;
  loading = false;
  error = '';
  private sub?: Subscription;

  constructor(private http: HttpClient) {}

  ngOnInit() { this.startPolling(); }
  ngOnDestroy() { this.sub?.unsubscribe(); }

  startPolling() {
    this.sub?.unsubscribe();
    this.fetch().subscribe(); // primera
    this.sub = interval(10000).pipe(switchMap(() => this.fetch())).subscribe();
  }

  fetch() {
    this.loading = true; this.error = '';
    let params = new HttpParams();
    if (this.msisdn.trim()) params = params.set('msisdn', this.msisdn.trim());

    return this.http.get<any>('/api/consumption', { params }).pipe({
      next: (res: any) => {
        if (this.msisdn.trim()) { this.item = res as Consumption; this.list = []; }
        else { this.item = undefined; this.list = (res?.results || []) as Consumption[]; }
        this.loading = false;
      },
      error: (err: any) => {
        this.item = undefined; this.list = [];
        this.error = err?.error?.message || 'Error al cargar';
        this.loading = false;
      }
    } as any);
  }

  simulateOne() {
    if (!this.msisdn.trim()) return;
    this.http.post('/api/consumption/simulate', { msisdn: this.msisdn.trim() })
      .subscribe(() => this.fetch().subscribe());
  }

  updatePartial() {
    if (!this.msisdn.trim()) return;
    this.http.post('/api/consumption/simulate', {
      msisdn: this.msisdn.trim(), balance: 10.4, minutes: 217
    }).subscribe(() => this.fetch().subscribe());
  }

  clearFilter() { this.msisdn = ''; this.fetch().subscribe(); }
}
