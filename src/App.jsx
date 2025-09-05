import { useState } from 'react'
import './App.css'

const API_BASE_URL = "https://5008-i1bk0kz108144exqximma-6c497bd2.manusvm.computer/api"

function App() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)
  const [email, setEmail] = useState('teste@walkie.com')
  const [password, setPassword] = useState('123456')

  const testConnection = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/test`)
      const data = await response.json()
      setMessage(`Teste de conectividade: ${data.message}`)
    } catch (error) {
      setMessage(`Erro no teste: ${error.message}`)
    }
    setLoading(false)
  }

  const testLogin = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
      })
      const data = await response.json()
      setMessage(`Login: ${data.message} - Usuário: ${data.user.email}`)
    } catch (error) {
      setMessage(`Erro no login: ${error.message}`)
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full">
        <h1 className="text-2xl font-bold text-center mb-6">Teste de Conectividade Walkie</h1>
        
        <div className="space-y-4">
          <button 
            onClick={testConnection}
            disabled={loading}
            className="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
          >
            {loading ? 'Testando...' : 'Testar Conexão Básica'}
          </button>

          <div className="space-y-2">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded"
            />
            <input
              type="password"
              placeholder="Senha"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded"
            />
            <button 
              onClick={testLogin}
              disabled={loading}
              className="w-full bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
            >
              {loading ? 'Testando...' : 'Testar Login'}
            </button>
          </div>
        </div>
        
        {message && (
          <div className="mt-4 p-4 bg-gray-50 rounded border">
            <p className="text-sm">{message}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

