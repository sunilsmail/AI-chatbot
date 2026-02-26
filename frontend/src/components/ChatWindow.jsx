import { useEffect, useRef } from 'react'
export default function ChatWindow({messages, loading}) {
  const ref = useRef(null)
  useEffect(()=>{ref.current?.scrollTo(0, ref.current.scrollHeight)}, [messages, loading])
  return <div className="chat" ref={ref}>{messages.map((m,i)=><div key={i} className={`bubble ${m.role}`}>{m.content}</div>)}{loading&&<div className="bubble assistant">Thinking...</div>}</div>
}
