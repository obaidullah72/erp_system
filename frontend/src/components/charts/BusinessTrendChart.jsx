import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import StatePanel from '../ui/StatePanel'
export default function BusinessTrendChart({rows,series,currency}) {
  if(rows==null)return <StatePanel state="unavailable" title="Trend data unavailable">Confirmed transactions are required to show this chart.</StatePanel>
  if(rows.length===0)return <StatePanel state="empty" title="No activity in this period"/>
  return <div><p className="mb-3 text-xs text-slate-500">Currency: {currency}. Use supporting records for exact decimal amounts.</p><div className="h-64" role="img" aria-label={`${series.map((item)=>item.label).join(', ')} by date`}><ResponsiveContainer width="100%" height="100%"><LineChart data={rows}><XAxis dataKey="date"/><YAxis/><Tooltip/><Legend/>{series.map((item)=><Line key={item.key} type="linear" dataKey={item.key} name={item.label} stroke={item.color} connectNulls={false} isAnimationActive={false}/>)}</LineChart></ResponsiveContainer></div></div>
}
