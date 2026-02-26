import axios from 'axios'
export const api = axios.create({ baseURL: 'http://localhost:8000' })
export const sendMessage = (payload, token) => api.post('/chat/message', payload, {headers:{Authorization:`Bearer ${token}`}})
export const getHistory = (sessionId, token) => api.get(`/chat/history/${sessionId}`, {headers:{Authorization:`Bearer ${token}`}})
