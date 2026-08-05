import axios from 'axios'

const BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' }
})

export const homerApi = {

  // Non-streaming fallback
  chat: async (message, sessionId = null) => {
    const response = await api.post('/chat/', {
      message,
      session_id: sessionId
    })
    return response.data
  },

  // Streaming chat — calls onToken for each token, onDone when complete
  chatStream: (message, sessionId, onToken, onDone, onError) => {
    fetch(`${BASE_URL}/chat/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        session_id: sessionId
      })
    })
    .then(response => {
      if (!response.ok) {
        return response.text().then(t => onError(`HTTP ${response.status}: ${t}`))
      }

      const reader  = response.body.getReader()
      const decoder = new TextDecoder()

      const read = () => {
        reader.read().then(({ done, value }) => {
          if (done) return

          const text  = decoder.decode(value)
          const lines = text.split('\n')

          lines.forEach(line => {
            if (!line.startsWith('data: ')) return
            try {
              const raw = line.slice(6).trim()
              if (!raw) return
              const data = JSON.parse(raw)

              if (data.error) {
                console.error('[Homer stream error]', data.error)
                onError(data.error)
              } else if (data.done) {
                onDone(data.citations || [], data.session_id)
              } else if (typeof data.token === 'string') {
                onToken(data.token)
              }
            } catch (e) {
              console.warn('[Homer parse error]', e, line)
            }
          })

          read()
        }).catch(err => {
          console.error('[Homer reader error]', err)
          onError(err.message)
        })
      }
      read()
    })
    .catch(err => {
      console.error('[Homer fetch error]', err)
      onError(err.message)
    })
  },

  getHistory: async (sessionId) => {
    const response = await api.get(`/chat/history?session_id=${sessionId}`)
    return response.data
  },

  resetSession: async (sessionId) => {
    const response = await api.delete(`/chat/reset/${sessionId}`)
    return response.data
  },

  getFamilyTree: async () => {
    const response = await api.get('/family-tree/')
    return response.data
  },

  getFigure: async (name) => {
    const response = await api.get(`/family-tree/${name}`)
    return response.data
  },

  getPath: async (from, to) => {
    const response = await api.get(`/family-tree/${from}/path/${to}`)
    return response.data
  }
}