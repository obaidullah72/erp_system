import { Link } from 'react-router-dom'
export default function PageHeading({ eyebrow, title, description, children, back }) {
  return <div className="mb-7 flex flex-wrap items-start justify-between gap-5"><div className="min-w-0">{back && <Link className="mb-3 inline-block text-sm font-medium text-teal-700 dark:text-teal-300" to={back}>Back to workspace</Link>}<p className="text-xs font-semibold uppercase tracking-widest text-teal-700 dark:text-teal-300">{eyebrow}</p><h1 className="mt-2 text-3xl font-semibold tracking-tight">{title}</h1>{description && <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500 dark:text-slate-400">{description}</p>}</div><div className="flex flex-wrap gap-3">{children}</div></div>
}
