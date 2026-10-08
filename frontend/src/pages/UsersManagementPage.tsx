import { useState, useEffect } from 'react'
import { usuarioService, type UsuarioItem } from '@/services/usuario.service'
import { formatDate } from '@/utils/format'

type ModalType = 'create' | 'edit' | 'password' | null

export default function UsersManagementPage() {
  const [users, setUsers] = useState<UsuarioItem[]>([])
  const [loading, setLoading] = useState(true)
  const [modal, setModal] = useState<ModalType>(null)
  const [selected, setSelected] = useState<UsuarioItem | null>(null)
  const [form, setForm] = useState({ nombre: '', usuario: '', password: '', rol: 'EMPLEADO' })

  const load = () => {
    setLoading(true)
    usuarioService.list().then((res) => {
      if (res.success && res.data) setUsers(res.data.items)
      setLoading(false)
    }).catch(() => setLoading(false))
  }

  useEffect(() => { load() }, [])

  const openCreate = () => { setSelected(null); setForm({ nombre: '', usuario: '', password: '', rol: 'EMPLEADO' }); setModal('create') }
  const openEdit = (u: UsuarioItem) => { setSelected(u); setForm({ nombre: u.nombre, usuario: u.usuario, password: '', rol: u.rol }); setModal('edit') }
  const openPassword = (u: UsuarioItem) => { setSelected(u); setForm({ ...form, password: '' }); setModal('password') }

  const handleCreate = async () => {
    if (!form.nombre || !form.usuario || !form.password) return alert('Complete todos los campos.')
    try {
      const res = await usuarioService.create(form)
      if (res.success) { load(); setModal(null) }
    } catch (err: any) { alert(err?.response?.data?.detail || 'Error al crear.') }
  }

  const handleEdit = async () => {
    if (!selected) return
    try {
      const res = await usuarioService.update(selected.id, { nombre: form.nombre, rol: form.rol })
      if (res.success) { load(); setModal(null) }
    } catch (err: any) { alert(err?.response?.data?.detail || 'Error al actualizar.') }
  }

  const handleToggleActive = async (u: UsuarioItem) => {
    try {
      const res = await usuarioService.update(u.id, { activo: !u.activo })
      if (res.success) load()
    } catch (err: any) { alert(err?.response?.data?.detail || 'Error.') }
  }

  const handleDesbloquear = async (u: UsuarioItem) => {
    try {
      const res = await usuarioService.desbloquear(u.id)
      if (res.success) load()
    } catch (err: any) { alert(err?.response?.data?.detail || 'Error al desbloquear.') }
  }

  const handlePassword = async () => {
    if (!selected || !form.password || form.password.length < 6) return alert('Mínimo 6 caracteres.')
    try {
      const res = await usuarioService.cambiarPassword(selected.id, form.password)
      if (res.success) { setModal(null); alert('Contraseña cambiada.') }
    } catch (err: any) { alert(err?.response?.data?.detail || 'Error.') }
  }

  const isBloqueado = (u: UsuarioItem) => u.bloqueado_hasta && new Date(u.bloqueado_hasta) > new Date()

  const set = (k: string) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => setForm({ ...form, [k]: e.target.value })

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-surface-800">Usuarios</h1>
        <button onClick={openCreate} className="btn-primary">+ Nuevo Usuario</button>
      </div>

      {loading ? <div className="text-center text-surface-500">Cargando...</div>
      : users.length === 0 ? <div className="text-center text-surface-500">Sin usuarios.</div>
      : (
        <div className="card overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b bg-surface-50 text-left text-surface-500">
                <th className="px-4 py-3">Usuario</th>
                <th className="px-4 py-3">Nombre</th>
                <th className="px-4 py-3">Rol</th>
                <th className="px-4 py-3">Estado</th>
                <th className="px-4 py-3">Último Acceso</th>
                <th className="px-4 py-3">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id} className="border-b hover:bg-surface-50">
                  <td className="px-4 py-3 font-medium">{u.usuario}</td>
                  <td className="px-4 py-3">{u.nombre}</td>
                  <td className="px-4 py-3">
                    <span className={`rounded px-2 py-0.5 text-xs ${u.rol === 'ADMINISTRADOR' ? 'bg-purple-100 text-purple-700' : 'bg-primary-100 text-primary-700'}`}>{u.rol}</span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex flex-wrap gap-1">
                      {!u.activo && <span className="rounded bg-red-100 px-2 py-0.5 text-xs text-red-700">Inactivo</span>}
                      {u.activo && !isBloqueado(u) && <span className="rounded bg-green-100 px-2 py-0.5 text-xs text-green-700">Activo</span>}
                      {isBloqueado(u) && <span className="rounded bg-orange-100 px-2 py-0.5 text-xs text-orange-700">Bloqueado</span>}
                    </div>
                  </td>
                  <td className="px-4 py-3 text-xs text-surface-500">{formatDate(u.ultimo_acceso)}</td>
                  <td className="px-4 py-3">
                    <div className="flex flex-wrap gap-1">
                      <button onClick={() => openEdit(u)} className="btn-warning btn-xs">Editar</button>
                      <button onClick={() => openPassword(u)} className="btn-primary btn-xs">Password</button>
                      <button onClick={() => handleToggleActive(u)} className={`rounded px-2 py-1 text-xs text-white ${u.activo ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'}`}>{u.activo ? 'Desactivar' : 'Activar'}</button>
                      {isBloqueado(u) && <button onClick={() => handleDesbloquear(u)} className="rounded bg-orange-500 px-2 py-1 text-xs text-white hover:bg-orange-600">Desbloquear</button>}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {modal === 'create' && (
        <div className="fixed inset-0 flex items-center justify-center bg-black/40" onClick={() => setModal(null)}>
          <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-premium" onClick={(e) => e.stopPropagation()}>
            <h2 className="mb-4 text-lg font-bold">Nuevo Usuario</h2>
            <div className="space-y-3">
              <input placeholder="Nombre" value={form.nombre} onChange={set('nombre')} className="w-full rounded-md border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary-500" />
              <input placeholder="Usuario" value={form.usuario} onChange={set('usuario')} className="w-full rounded-md border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary-500" />
              <input type="password" placeholder="Contraseña" value={form.password} onChange={set('password')} className="w-full rounded-md border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary-500" />
              <select value={form.rol} onChange={set('rol')} className="w-full rounded-md border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary-500">
                <option value="EMPLEADO">EMPLEADO</option>
                <option value="ADMINISTRADOR">ADMINISTRADOR</option>
              </select>
            </div>
            <div className="mt-4 flex justify-end gap-2">
              <button onClick={() => setModal(null)} className="rounded-md border px-4 py-2 text-sm text-surface-700">Cancelar</button>
              <button onClick={handleCreate} className="btn-primary">Crear</button>
            </div>
          </div>
        </div>
      )}

      {modal === 'edit' && selected && (
        <div className="fixed inset-0 flex items-center justify-center bg-black/40" onClick={() => setModal(null)}>
          <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-premium" onClick={(e) => e.stopPropagation()}>
            <h2 className="mb-4 text-lg font-bold">Editar: {selected.usuario}</h2>
            <div className="space-y-3">
              <input placeholder="Nombre" value={form.nombre} onChange={set('nombre')} className="w-full rounded-md border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary-500" />
              <select value={form.rol} onChange={set('rol')} className="w-full rounded-md border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary-500">
                <option value="EMPLEADO">EMPLEADO</option>
                <option value="ADMINISTRADOR">ADMINISTRADOR</option>
              </select>
            </div>
            <div className="mt-4 flex justify-end gap-2">
              <button onClick={() => setModal(null)} className="rounded-md border px-4 py-2 text-sm text-surface-700">Cancelar</button>
              <button onClick={handleEdit} className="btn-warning">Guardar</button>
            </div>
          </div>
        </div>
      )}

      {modal === 'password' && selected && (
        <div className="fixed inset-0 flex items-center justify-center bg-black/40" onClick={() => setModal(null)}>
          <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-premium" onClick={(e) => e.stopPropagation()}>
            <h2 className="mb-4 text-lg font-bold">Cambiar Contraseña: {selected.usuario}</h2>
            <input type="password" placeholder="Nueva contraseña (mín 6)" value={form.password} onChange={set('password')} className="w-full rounded-md border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-primary-500" />
            <div className="mt-4 flex justify-end gap-2">
              <button onClick={() => setModal(null)} className="rounded-md border px-4 py-2 text-sm text-surface-700">Cancelar</button>
              <button onClick={handlePassword} className="btn-primary">Cambiar</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
