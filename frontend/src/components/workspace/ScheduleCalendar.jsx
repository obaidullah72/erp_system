import { eachDayOfInterval, endOfMonth, format, getISODay, isValid, parseISO, startOfMonth } from 'date-fns'
export default function ScheduleCalendar({month,entries=[]}) {
  const date=parseISO(`${month}-01`)
  if(!isValid(date))return <p role="alert">Choose a valid calendar month.</p>
  const days=eachDayOfInterval({start:startOfMonth(date),end:endOfMonth(date)})
  return <div className="mt-4 overflow-x-auto"><table className="w-full min-w-[420px] table-fixed border-collapse text-sm"><caption className="mb-3 text-left text-sm text-slate-500">{format(date,'MMMM yyyy')} · Schedule data unavailable</caption><thead><tr>{['Mon','Tue','Wed','Thu','Fri','Sat','Sun'].map((day)=><th key={day} className="p-2 text-xs font-medium text-slate-500">{day}</th>)}</tr></thead><tbody>{Array.from({length:Math.ceil((getISODay(days[0])-1+days.length)/7)},(_,week)=><tr key={week}>{Array.from({length:7},(_,day)=>{const index=week*7+day-(getISODay(days[0])-1);const value=days[index];return <td key={day} className="h-16 border border-slate-200 p-2 align-top dark:border-slate-700">{value&&<><time dateTime={format(value,'yyyy-MM-dd')}>{format(value,'d')}</time>{entries.filter((entry)=>entry.date===format(value,'yyyy-MM-dd')).map((entry)=><p key={entry.id}>{entry.name}</p>)}</>}</td>})}</tr>)}</tbody></table></div>
}
