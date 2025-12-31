# Unified Study Calculator API

## Base URL
`http://localhost:5000`

## Endpoints

### Health Check
- **GET** `/api/health`
- Returns API status

### Cost Calculator Endpoints

#### Calculate Cost
- **POST** `/api/cost-calculator/calculate`
- Body: `{"selected_buckets": ["Bucket-1", "Bucket-2"]}`
- Returns: `{"total_cost": 50000}`

#### Store User Details (Cost Calculator)
- **POST** `/api/cost-calculator/user-details`
- Body: `{"name": "John", "email": "john@example.com", "phone": "1234567890", "intent": "viewed_estimate"}`

#### Request Callback
- **POST** `/api/cost-calculator/request-callback`
- Body: `{"name": "John", "mobileNumber": "1234567890"}`

#### Store Download Request
- **POST** `/api/cost-calculator/download-request`
- Body: `{"name": "John", "email": "john@example.com", "phone": "1234567890"}`

#### Download Cost PDF
- **POST** `/api/cost-calculator/download-pdf`
- Requires session data from previous calculate and download-request calls

### Grade Calculator Endpoints

#### Calculate German Grade
- **POST** `/api/grade-calculator/calculate`
- Body: `{"best_grade": "10", "min_passing_grade": "4", "your_grade": "8"}`
- Returns: `{"german_grade": 2.3}`

#### Store User Details (Grade Calculator)
- **POST** `/api/grade-calculator/user-details`
- Body: `{"name": "John", "email": "john@example.com", "phone": "1234567890"}`

#### Download Grade PDF
- **POST** `/api/grade-calculator/download-pdf`
- Body: `{"best_grade": "10", "min_passing_grade": "4", "your_grade": "8", "german_grade": "2.3"}`

## Bucket Mappings (Cost Calculator)
- Bucket-1: Passport
- Bucket-2: Career counselling and pre-application assistance + university application
- Bucket-3: APS certification
- Bucket-4: IELTS/TOEFL + language training (A1 + A2)
- Bucket-5: Blocked account, financial assistance, visa process, air ticket, travel insurance
- Bucket-6: Other services