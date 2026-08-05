import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import WelcomePage from './pages/WelcomePage'
import ChatPage from './pages/ChatPage'
import FamilyTreePage from './pages/FamilyTreePage'

function App() {
  return (
    <div className="w-full h-screen">
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={<WelcomePage />}
          />
          <Route
            path="/chat"
            element={<ChatPage />}
          />
          <Route
            path="/family-tree"
            element={<FamilyTreePage />}
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App