import json, os, pathlib
from gradio_client import Client

role=os.environ['ROLE']
model=os.environ.get('MODEL','huggingface-projects/llama-3.2-3B-Instruct')
mission=pathlib.Path('MISSION.md').read_text()
prompt=f'''You are role {role} in CEREBRON Farm 26 Climate Environment.
{mission}
Produce a concise evidence-based assessment with: system boundary, spatial/temporal scale, observations vs models, causal chain, uncertainties, risks, adaptation/mitigation implications when relevant, validation path, unknowns, and final claim ledger. Do not present scenarios as forecasts or models as observations.'''
out={'role':role,'model':model,'success':False,'text':'','error':None}
try:
    c=Client(model)
    r=c.predict(message=prompt, api_name='/chat')
    out['success']=True
    out['text']=str(r)
except Exception as e:
    out['error']=repr(e)
pathlib.Path('results').mkdir(exist_ok=True)
pathlib.Path(f'results/{role}.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({'role':role,'success':out['success']}))
