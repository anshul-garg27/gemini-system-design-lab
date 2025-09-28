import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Dashboard from './components/Dashboard';
import Topics from './components/Topics';
import Analytics from './components/Analytics';
import ContentGenerator from './components/ContentGenerator';
import ApiHealthCheck from './components/ApiHealthCheck';
import Layout from './components/Layout';
import { ThemeProvider } from './contexts/ThemeContext';

function App() {
  return (
    <ThemeProvider>
      <Router>
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/topics" element={<Topics />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/content-generator" element={<ContentGenerator />} />
              <Route path="/health-check" element={<ApiHealthCheck />} />
            </Routes>
          </Layout>
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
              success: {
                duration: 3000,
                iconTheme: {
                  primary: '#10B981',
                  secondary: '#fff',
                },
              },
              error: {
                duration: 5000,
                iconTheme: {
                  primary: '#EF4444',
                  secondary: '#fff',
                },
              },
            }}
          />
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;