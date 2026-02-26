import { useState } from 'react'
import ChatWindow from './components/ChatWindow'
import { sendMessage } from './api/client'
export default function App(){
  const [messages,setMessages]=useState([])
  const [text,setText]=useState('')
  const [loading,setLoading]=useState(false)
  const token=localStorage.getItem('token')||'dev-token'
  const sessionId=Number(localStorage.getItem('sessionId')||1)
  const onSend=async()=>{
    if(!text) return
    const next=[...messages,{role:'user',content:text}]; setMessages(next); setText(''); setLoading(true)
    const {data}=await sendMessage({session_id:sessionId,user_id:1,message:text}, token)
    setMessages([...next,{role:'assistant',content:data.response||JSON.stringify(data)}]); setLoading(false)
  }
  return <div className="container"><h1>eCommerce AI Chatbot</h1><ChatWindow messages={messages} loading={loading}/><div className="controls"><input value={text} onChange={e=>setText(e.target.value)} placeholder="Ask about order, cancellation, refunds..."/><button onClick={onSend}>Send</button></div></div>
}
