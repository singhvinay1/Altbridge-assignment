import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.PROD ? 'https://your-backend-app.onrender.com' : 'http://localhost:8000',
  timeout: 120000
})

export default api



