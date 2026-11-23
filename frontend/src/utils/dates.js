import { format, isValid, parseISO } from 'date-fns'
export function displayDate(value) { if (!value) return 'Unavailable'; const parsed=parseISO(value); return isValid(parsed)?format(parsed,'dd MMM yyyy'):'Invalid date' }
export function displayInstant(value,timezone='UTC') { if(!value)return 'Unavailable';const date=new Date(value);return Number.isNaN(date.valueOf())?'Invalid date':new Intl.DateTimeFormat('en-GB',{dateStyle:'medium',timeStyle:'short',timeZone:timezone}).format(date) }
