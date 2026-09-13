// FinGuard AI — Load Test
//
// Simulates concurrent users hitting the live health endpoint to observe
// how Cloud Run handles simultaneous traffic and scales under load.
//
// Deliberately targets /api/v1/health (not /api/v1/chat) — this tests
// Cloud Run's request-handling and autoscaling behavior without
// triggering real Vertex AI/Gemini API costs on every test run.

import http from 'k6/http';
import { check, sleep } from 'k6';

const TARGET_URL = __ENV.TARGET_URL || 'https://finguard-ai-283915220530.us-central1.run.app/api/v1/health';

export const options = {
  stages: [
    { duration: '10s', target: 10 },
    { duration: '20s', target: 30 },
    { duration: '15s', target: 30 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'],
    http_req_failed: ['rate<0.05'],
  },
};

export default function () {
  const res = http.get(TARGET_URL);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response has status field': (r) => JSON.parse(r.body).status !== undefined,
  });
  sleep(1);
}
