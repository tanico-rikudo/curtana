This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

This is a demo app demonstrating the use of NextJS and AG Grid to create a simple data grid that displays information about people.

## Getting Started

First, install dependencies using `npm install`.

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

Note that the demo of this app connects to a database. If you deploy the project on your own machine, your grid will populate with dummy data in the absence of a database connection. 

Alternatively, you can create your own data source. If you do this, the data should be an array of objects with the following structure:

```json
{
  "id": "<id>",
  "first_name": "<first name>",
  "last_name": "<last name>",
  "email": "<email address>",
  "phone": "<phone number>",
  "office": "<city name>",
  "job_title": "<job title>"
 }
```

prisma
```bash
npm install prisma --save-dev
npx init prisma
npx prisma generate
```

<!-- https://tech.012grp.co.jp/entry/2021/03/25/125014 -->
