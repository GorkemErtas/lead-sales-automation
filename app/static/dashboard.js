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