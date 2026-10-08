import { useState, useCallback, type InputHTMLAttributes } from 'react'
import { formatCOPInput, parseCOP } from '@/utils/currency'

interface CurrencyInputProps extends Omit<InputHTMLAttributes<HTMLInputElement>, 'value' | 'onChange'> {
  value: number | string
  onChange: (value: number) => void
}

export default function CurrencyInput({ value, onChange, className, ...props }: CurrencyInputProps) {
  const [display, setDisplay] = useState(() => formatCOPInput(String(value)))

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const raw = e.target.value.replace(/[^0-9]/g, '')
    const formatted = formatCOPInput(raw)
    setDisplay(formatted)
    onChange(parseCOP(raw))
  }, [onChange])

  const handleKeyDown = useCallback((e: React.KeyboardEvent<HTMLInputElement>) => {
    const numericKeys = ['0','1','2','3','4','5','6','7','8','9','Backspace','Delete','Tab','ArrowLeft','ArrowRight','Home','End']
    if (!numericKeys.includes(e.key) && !e.ctrlKey && !e.metaKey) {
      e.preventDefault()
    }
  }, [])

  return (
    <div className="relative">
      <span className="absolute left-3 top-1/2 -translate-y-1/2 text-surface-400 font-medium text-sm pointer-events-none">$</span>
      <input
        type="text"
        inputMode="numeric"
        value={display}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        className={`${className || 'input'} pl-7`}
        {...props}
      />
    </div>
  )
}
