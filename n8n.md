🚀 Option 1: Install n8n using npm (Recommended)
✅ Prerequisites

Install Node.js (v18 or later)

Install npm (comes with Node)

📌 Install command
npm install n8n -g
▶️ Run n8n
n8n
🌐 Open in browser
http://localhost:5678
🐳 Option 2: Install using Docker (Best for production)
📌 Run command
docker run -it --rm \
  -p 5678:5678 \
  n8nio/n8n
▶️ Open
http://localhost:5678
⚡ Option 3: Run without install (npx)
npx n8n
🔐 Optional: Set login (recommended)
export N8N_BASIC_AUTH_ACTIVE=true
export N8N_BASIC_AUTH_USER=admin
export N8N_BASIC_AUTH_PASSWORD=password
n8n
📦 Verify installation
n8n --version
💡 Pro Tips

Use Docker for stability in production

Use npm global install for local development

You can connect databases like MySQL/Postgres later

If you want, I can help you:

Deploy n8n on AWS / server

Create your first workflow

Connect APIs (like WhatsApp, email, etc.)
