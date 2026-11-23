export default function Button({ children, className = '', variant = 'primary', type = 'button', ...props }) {
  const style = variant === 'primary' ? 'bg-teal-700 text-white hover:bg-teal-800' : variant === 'danger' ? 'bg-red-700 text-white hover:bg-red-800' : 'border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 dark:border-slate-600 dark:bg-slate-900 dark:text-slate-200 dark:hover:bg-slate-800'
  return <button type={type} className={`inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-teal-600 disabled:cursor-not-allowed disabled:opacity-50 ${style} ${className}`} {...props}>{children}</button>
}
