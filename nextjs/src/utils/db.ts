import { Pool } from 'pg';

let connection = new Pool({
  connectionString: process.env.DATABASE_URL,
});

export default connection;
