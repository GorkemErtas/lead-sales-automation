const money=new Intl.NumberFormat("tr-TR",{style:"currency",currency:"TRY",maximumFractionDigits:0});
const pct=v=>v==null?"—":"%"+Number(v).toFixed(2);
const num=v=>Number(v||0);
function bar(name,value,max,label,extra){const width=Math.max(0,Math.min(100,value/max*100));return '<div><div class="bar-head"><span>'+name+'</span><strong>'+label+'</strong></div><div class="track"><div class="fill '+extra+'" style="width:'+width+'%"></div></div></div>'}
async function loadDashboard(){
 try{
  const res=await fetch("/api/v1/analytics/dashboard",{cache:"no-store"});
  if(!res.ok)throw new Error("Analytics request failed");
  const data=await res.json(),s=data.summary,reps=data.representatives;
  document.getElementById("totalLeads").textContent=s.total_leads;
  document.getElementById("convertedLeads").textContent=s.converted_leads;
  document.getElementById("conversionRate").textContent=pct(s.conversion_rate)+" conversion";
  document.getElementById("revenue").textContent=money.format(num(s.revenue));
  document.getElementById("adCost").textContent=money.format(num(s.ad_cost))+" ad cost";
  document.getElementById("profit").textContent=money.format(num(s.profit));
  document.getElementById("roi").textContent=pct(s.roi)+" ROI";
  document.getElementById("updated").textContent="Updated "+new Date().toLocaleTimeString("tr-TR",{hour:"2-digit",minute:"2-digit",second:"2-digit"});
  document.getElementById("repRows").innerHTML=reps.map(r=>'<tr><td><strong>'+r.representative_name+'</strong></td><td>'+r.total_leads+'</td><td>'+r.converted_leads+'</td><td>'+pct(r.conversion_rate)+'</td><td>'+money.format(num(r.ad_cost))+'</td><td>'+money.format(num(r.revenue))+'</td><td class="positive">'+money.format(num(r.profit))+'</td><td class="positive">'+pct(r.roi)+'</td></tr>').join("");
  document.getElementById("conversionBars").innerHTML=reps.map(r=>bar(r.representative_name,num(r.conversion_rate),100,pct(r.conversion_rate),"")).join("");
  const maxProfit=Math.max(...reps.map(r=>num(r.profit)),1);
  document.getElementById("profitBars").innerHTML=reps.map(r=>bar(r.representative_name,num(r.profit),maxProfit,money.format(num(r.profit)),"profit-fill")).join("");
 }catch(e){document.getElementById("updated").textContent="Unable to load live data";console.error(e)}
}
loadDashboard();setInterval(loadDashboard,15000);
const LEAD_WEBHOOK="https://n8n-production-c116.up.railway.app/webhook/meta-lead";
const SALE_WEBHOOK="https://n8n-production-c116.up.railway.app/webhook/sale-conversion";
const modal=id=>document.getElementById(id);
document.getElementById("openLead").onclick=()=>modal("leadModal").classList.add("open");
document.getElementById("openSale").onclick=()=>modal("saleModal").classList.add("open");
document.querySelectorAll("[data-close]").forEach(b=>b.onclick=()=>modal(b.dataset.close).classList.remove("open"));
document.querySelectorAll(".modal-backdrop").forEach(m=>m.onclick=e=>{if(e.target===m)m.classList.remove("open")});

async function postDemo(url,payload,statusId){
 const el=document.getElementById(statusId);el.className="form-status";el.textContent="Sending through n8n…";
 try{
  const res=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});
  if(!res.ok)throw new Error("Workflow returned "+res.status);
  el.className="form-status ok";el.textContent="Success — live metrics will refresh automatically.";
  setTimeout(loadDashboard,700);
  return true;
 }catch(e){el.className="form-status error";el.textContent="Could not complete workflow. Check n8n execution.";return false}
}
document.getElementById("leadForm").onsubmit=async e=>{
 e.preventDefault();const fd=new FormData(e.currentTarget);
 const id="META-DEMO-"+Date.now();
 const ok=await postDemo(LEAD_WEBHOOK,{lead_id:id,campaign:fd.get("campaign"),ad_cost:Number(fd.get("ad_cost")),representative:fd.get("representative")},"leadStatus");
 if(ok){e.currentTarget.reset();document.getElementById("leadStatus").textContent="Created "+id+" — use this ID to convert the sale."}
};
document.getElementById("saleForm").onsubmit=async e=>{
 e.preventDefault();const fd=new FormData(e.currentTarget);
 const ok=await postDemo(SALE_WEBHOOK,{meta_lead_id:fd.get("meta_lead_id"),revenue:Number(fd.get("revenue"))},"saleStatus");
 if(ok)e.currentTarget.reset();
};