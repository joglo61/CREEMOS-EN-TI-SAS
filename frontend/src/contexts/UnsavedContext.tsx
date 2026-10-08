import { createContext, useContext, useState, useCallback, type ReactNode } from 'react'

interface UnsavedContextType {
  isDirty: boolean
  setDirty: () => void
  markClean: () => void
}

const UnsavedContext = createContext<UnsavedContextType | null>(null)

export function UnsavedProvider({ children }: { children: ReactNode }) {
  const [isDirty, setIsDirty] = useState(false)

  const setDirty = useCallback(() => setIsDirty(true), [])
  const markClean = useCallback(() => setIsDirty(false), [])

  return (
    <UnsavedContext.Provider value={{ isDirty, setDirty, markClean }}>
      {children}
    </UnsavedContext.Provider>
  )
}

export function useUnsaved() {
  const ctx = useContext(UnsavedContext)
  if (!ctx) throw new Error('useUnsaved must be used within UnsavedProvider')
  return ctx
}
