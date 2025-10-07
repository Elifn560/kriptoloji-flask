const methodFields = {
  caesar: [
    {name: 'shift', label: 'Kaydırma (tamsayı)', type: 'number', placeholder: 'Örn: 3', required: true}
  ],
  vigenere: [
    {name:'key', label:'Anahtar (kelime)', type:'text', placeholder:'Örn: SECRET', required:true}
  ],
  substitution: [
    {name:'key', label:'26 harflik anahtar (A..Z sırası)', type:'text', placeholder:'Örn: QWERTYUIOPASDFGHJKLZXCVBNM', required:true}
  ],
  affine: [
    {name:'a', label:'a (coprime with 26)', type:'number', placeholder:'Örn: 5', required:true},
    {name:'b', label:'b', type:'number', placeholder:'Örn: 8', required:true}
  ],
  playfair: [
    {name:'key', label:'Anahtar (kelime)', type:'text', placeholder:'Örn: KEYWORD', required:true}
  ],
  route: [
    {name:'cols', label:'Sütun sayısı (tamsayı)', type:'number', placeholder:'Örn: 4', required:true}
  ],
  railfence: [
    {name:'rails', label:'Ray sayısı (tamsayı)', type:'number', placeholder:'Örn: 3', required:true}
  ]
};

const modal = document.getElementById('modal');
const dynamic = document.getElementById('dynamicFields');
const modalTitle = document.getElementById('modalTitle');
let currentMethod = null;

document.querySelectorAll('.card .open').forEach(btn=>{
  btn.addEventListener('click', (e)=>{
    const card = e.target.closest('.card');
    const method = card.dataset.method;
    openModal(method);
  });
});

function openModal(method){
  currentMethod = method;
  modalTitle.textContent = 'Şifreleme - ' + method;
  dynamic.innerHTML = '';
  const fields = methodFields[method] || [];
  fields.forEach(f=>{
    const lab = document.createElement('label');
    lab.textContent = f.label;
    const inp = document.createElement(f.type === 'number' ? 'input' : 'input');
    inp.type = f.type === 'number' ? 'number' : 'text';
    inp.name = f.name;
    inp.placeholder = f.placeholder || '';
    if (f.required) inp.required = true;
    dynamic.appendChild(lab);
    dynamic.appendChild(inp);
  });
  document.getElementById('text').value = '';
  document.getElementById('resultArea').value = '';
  modal.classList.remove('hidden');
}

document.getElementById('closeBtn').addEventListener('click', ()=> modal.classList.add('hidden'));

async function doAction(endpoint){
  const text = document.getElementById('text').value;
  const inputs = dynamic.querySelectorAll('input');
  const params = {};
  inputs.forEach(i=>{
    if (i.type === 'number') params[i.name] = parseInt(i.value || '0');
    else params[i.name] = i.value || '';
  });

  const payload = { method: currentMethod, text, params };
  try{
    const res = await fetch(`/api/${endpoint}`, {
      method:'POST',
      headers:{ 'Content-Type':'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (res.ok && data.result !== undefined){
      document.getElementById('resultArea').value = data.result;
    }else{
      document.getElementById('resultArea').value = 'Hata: ' + (data.error || 'Bilinmeyen hata');
    }
  }catch(err){
    document.getElementById('resultArea').value = 'İstek hatası: ' + err.message;
  }
}

document.getElementById('encryptBtn').addEventListener('click', ()=> doAction('encrypt'));
document.getElementById('decryptBtn').addEventListener('click', ()=> doAction('decrypt'));
