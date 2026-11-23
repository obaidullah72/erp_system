import { useEffect, useRef, useState } from 'react'
import JsBarcode from 'jsbarcode'
import QRCode from 'qrcode'
import Button from '../ui/Button'
export default function BarcodePreview({value}) {
  const barcode=useRef(null);const[qr,setQr]=useState('');const[error,setError]=useState('')
  useEffect(()=>{let active=true;Promise.resolve().then(async()=>{if(!value||value.length>80)throw new Error('Enter an identifier of 1–80 characters.');JsBarcode(barcode.current,value,{format:'CODE128',width:1.5,height:50,margin:12,displayValue:true});const image=await QRCode.toDataURL(value,{width:160,margin:2});if(active){setQr(image);setError('')}}).catch((failure)=>{if(active){setError(failure.message);setQr('')}});return()=>{active=false}},[value])
  return <section className="erp-panel p-5"><h2 className="font-semibold">Barcode & QR label preview</h2><p className="mt-2 text-sm text-slate-500">Local identifier preview. Printing a draft label does not create or update a product.</p>{error&&<p role="status" className="mt-3 text-sm text-slate-500">{error}</p>}<div className="erp-print mt-4 flex flex-wrap items-center gap-5"><svg ref={barcode} role="img" aria-label={`Code 128 for ${value||'empty identifier'}`} className={`max-w-full ${error?'hidden':''}`}/>{qr&&<img src={qr} width={160} height={160} alt={`QR code for ${value}`}/>}</div><Button className="mt-4" variant="secondary" disabled={!!error||!qr} onClick={()=>window.print()}>Print identifier labels</Button></section>
}
