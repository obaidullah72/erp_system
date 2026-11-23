import { Activity, LayoutDashboard, Map, Package, Warehouse, ShoppingCart, Store, Landmark, Factory, ChartNoAxesCombined, Settings2 } from 'lucide-react'
export const navigation = [
  { to:'/',label:'Dashboard',icon:LayoutDashboard,permission:'dashboard:read' },
  { to:'/workspace/master-data',label:'Master data',icon:Package,group:'Master data' },
  { to:'/workspace/inventory',label:'Inventory',icon:Warehouse,group:'Inventory' },
  { to:'/workspace/purchases',label:'Purchases',icon:ShoppingCart,group:'Purchases' },
  { to:'/workspace/sales',label:'Sales & POS',icon:Store,group:'Sales' },
  { to:'/workspace/accounting',label:'Accounting',icon:Landmark,group:'Accounting' },
  { to:'/workspace/manufacturing',label:'Manufacturing',icon:Factory,group:'Manufacturing' },
  { to:'/workspace/reports',label:'Reports',icon:ChartNoAxesCombined,group:'Reports' },
  { to:'/workspace/administration',label:'Administration',icon:Settings2,group:'Administration' },
  { to:'/system',label:'System status',icon:Activity },
  { to:'/roadmap',label:'Implementation roadmap',icon:Map },
]
