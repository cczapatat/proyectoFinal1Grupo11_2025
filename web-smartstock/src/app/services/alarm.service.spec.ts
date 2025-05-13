import { faker } from '@faker-js/faker';
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { environment } from '../../environments/environment';
import { AlarmService } from './alarm.service';
import { Alarm } from '../alarm/alarm';

describe('Service: Alarm', () => {
  let service: AlarmService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AlarmService]
    });

    service = TestBed.inject(AlarmService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should create a alarm', () => {
    const mockAlarm: Alarm = {
      id: faker.string.uuid(),
      manufacture_id: faker.string.uuid(),
      product_id: faker.string.uuid(),
      minimum_value: faker.number.float({ min: 1, max: 500 }),
      maximum_value: faker.number.float({ min: 501, max: 1000 }),
      notes: faker.lorem.word({ length: 10 })
    };

    service.createAlarm(mockAlarm).subscribe((response) => {
      expect(response).toEqual(mockAlarm);
    });

    const req = httpMock.expectOne(`${environment.apiAlarmUrl}/new`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(mockAlarm);
    req.flush(mockAlarm);
  });
});