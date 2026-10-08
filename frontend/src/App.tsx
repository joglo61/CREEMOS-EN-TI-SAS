import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from '@/contexts/AuthContext'
import { UnsavedProvider } from '@/contexts/UnsavedContext'
import { ToastProvider } from '@/contexts/ToastContext'
import ProtectedLayout from '@/layouts/ProtectedLayout'
import LoginPage from '@/pages/LoginPage'
import DashboardPage from '@/pages/DashboardPage'
import ClientesListPage from '@/pages/ClientesListPage'
import ClienteFormPage from '@/pages/ClienteFormPage'
import ClienteDetailPage from '@/pages/ClienteDetailPage'
import PrestamosListPage from '@/pages/PrestamosListPage'
import PrestamoDetailPage from '@/pages/PrestamoDetailPage'
import PrestamoFormPage from '@/pages/PrestamoFormPage'
import RegistrarPagoPage from '@/pages/RegistrarPagoPage'
import FacturaDetailPage from '@/pages/FacturaDetailPage'
import FacturasListPage from '@/pages/FacturasListPage'
import ExcelManagementPage from '@/pages/ExcelManagementPage'
import ConfigurationPage from '@/pages/ConfigurationPage'
import UsersManagementPage from '@/pages/UsersManagementPage'
import BackupsPage from '@/pages/BackupsPage'
import ReportsPage from '@/pages/ReportsPage'

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
          <ToastProvider>
          <UnsavedProvider>
          <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route element={<ProtectedLayout />}>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/clientes" element={<ClientesListPage />} />
            <Route path="/clientes/nuevo" element={<ClienteFormPage />} />
            <Route path="/clientes/:id" element={<ClienteDetailPage />} />
            <Route path="/clientes/:id/editar" element={<ClienteFormPage />} />
            <Route path="/prestamos" element={<PrestamosListPage />} />
            <Route path="/prestamos/nuevo" element={<PrestamoFormPage />} />
            <Route path="/prestamos/:id" element={<PrestamoDetailPage />} />
            <Route path="/prestamos/:id/pagar" element={<RegistrarPagoPage />} />
            <Route path="/facturas" element={<FacturasListPage />} />
            <Route path="/facturas/:id" element={<FacturaDetailPage />} />
            <Route path="/excel" element={<ExcelManagementPage />} />
            <Route path="/config" element={<ConfigurationPage />} />
            <Route path="/usuarios" element={<UsersManagementPage />} />
            <Route path="/backups" element={<BackupsPage />} />
            <Route path="/reportes" element={<ReportsPage />} />
          </Route>
          </Routes>
          </UnsavedProvider>
          </ToastProvider>
      </AuthProvider>
    </BrowserRouter>
  )
}
