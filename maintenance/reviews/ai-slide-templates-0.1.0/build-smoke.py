from pathlib import Path
from html.parser import HTMLParser
import html,json,shutil
import argparse
args=argparse.ArgumentParser()
args.add_argument('--library',required=True)
args.add_argument('--out',required=True)
options=args.parse_args()
root=Path(options.out).resolve()
library=Path(options.library).resolve()
briefs={
'direct':{'template':'airy-modern','brief':'Use Airy Modern. Create an eight-slide internal presentation for the fictional Luma team about a guided onboarding pilot. All figures are simulated: 20 interviews, 15 favor a guided start. Cover research, user journey, measurement plan, milestones and next decision.', 'slides':[
['Luma / Pilot planning','A clearer first day','Guided onboarding pilot · simulated research for internal review.','Guide','Learn','Repeat','Interviews','15/20','Guided start.','Pilot goal','Help new teams finish one useful task.','Decision','Test one guided path with a small cohort.'],
['Plan','From research to pilot','Eight slides to align the team on a focused experiment.','Research','Journey','Measures','Pilot','What we heard','Twenty simulated interviews informed the proposed pilot.','What we will test','One guided task with a visible completion point.'],
['Research','Three working hypotheses','Pilot assumptions to verify with real users.','1','A clear starting task helps','Offer one recommended workflow at first entry.','2','Visible progress supports learning','Show the next step and completed work.','3','Saved paths may support return visits','Let teams reuse a completed task as a template.'],
['Make the first useful task easy to find.','Pilot principle','Teach through one completed workflow.','Keep setup short, show progress and offer an editable starting point. Real pilot evidence will decide the next iteration.'],
['Journey','Five pilot moments','Observe where a new team proceeds or needs help.','01','Arrive','Read the task goal.','02','Choose','Confirm a starting path.','03','Build','Complete a first draft.','04','Refine','Edit the useful result.','05','Return','Reuse the saved path.'],
['Measures','Illustrative priorities','Bar lengths illustrate priority only; no measured results.','Completion','Return visits','Saved paths','Confidence'],
['Pilot','Three review points','Proposed sequence; dates await team agreement.','Week 1','Prepare the task and recruit a small cohort.','Week 2','Observe first use and collect feedback.','Week 3','Review task completion and return visits.','Decision','Expand only if the pilot supports the hypothesis.'],
['Next step','Approve the pilot scope.','Agree on the first task, owner and measurement plan before recruiting.']
]},
'selection':{'template':'circuit-tech-dark','brief':'Raw notes: fictional Relay architecture proposal; engineering audience; dark visual style; concise eight-slide narrative. Need client to gateway to runtime to storage and telemetry; show proposed health signals with no production claims; staged rollout, owners and next review. Compare appropriate dark technical templates before choosing.', 'slides':[
['relay.proposal','Relay Architecture Pilot','A fictional engineering proposal for a traceable task runtime.','review --stage=','pilot','modules: gateway / runtime\nstatus:','proposal only'],
['review.agenda','4 decisions','Agree on boundaries, signals, rollout and ownership.','01/constraints','Define the pilot scope and service boundaries.','02/services','Map requests, execution and stored results.','03/observability','Agree on tracing and failure diagnosis.','04/rollout','Stage access behind a pilot feature flag.'],
['service.map','proposed flow','Route requests through explicit execution boundaries.','Web Client','Request entry','API Gateway','Auth and routing','Task Runtime','Execution events','Result Store','Persisted output','Trace Service','Debug evidence'],
['service.owners','ownership draft','Assign one accountable owner per proposed service.','Experience','Client request form and result review.','WEB','Coordination','Gateway routing and runtime task lifecycle.','API','Execution','Task steps, failure handling and trace emission.','OPS','Persistence','Results, task metadata and retention rules.','DB'],
['pilot.signals','measurement plan','Illustrative display values; production baselines are not collected.','TBD','Success baseline','TBD','Latency baseline','TBD','Failure baseline','5','Proposed services'],
['trace.flow','diagnostic path','Follow one request from user intent to stored result.','Request','Route','Run','Trace','Store'],
['rollout.plan','proposed stages','Advance after reviewing evidence at each stage.','01 Design','Agree on interfaces and task states.','02 Sandbox','Exercise sample requests and failures.','03 Pilot','Enable access for one internal team.','04 Review','Inspect traces and decide the next scope.'],
['review.next','Make each task traceable.','Confirm service owners and a sandbox milestone at the design review.']
]}}
class Texts(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=False);self.s=s;self.lines=s.splitlines(keepends=True);self.line_offsets=[0]
  for line in self.lines:self.line_offsets.append(self.line_offsets[-1]+len(line))
  self.parts=[]
 def handle_data(self,data):
  if data.strip():
   line,col=self.getpos();self.parts.append((self.line_offsets[line-1]+col,len(data),data))
for case,brief in briefs.items():
 slug=brief['template'];out=root/'outputs'/case/'templates'/slug
 shutil.copytree(library/'templates'/slug,out,dirs_exist_ok=True)
 s=(out/'template.html').read_text()
 import re
 matches=list(re.finditer(r'<section\b[^>]*class="slide[^\"]*"[^>]*>.*?</section>',s,re.S))
 assert len(matches)==len(brief['slides'])
 for match,replacements in reversed(list(zip(matches,brief['slides']))):
  block=match.group();p=Texts(block);p.feed(block)
  assert len(p.parts)==len(replacements),(case,len(p.parts),len(replacements),p.parts)
  for (start,length,old),new in reversed(list(zip(p.parts,replacements))):block=block[:start]+html.escape(re.match(r"\s*",old)[0]+new+re.search(r"\s*$",old)[0])+block[start+length:]
  s=s[:match.start()]+block+s[match.end():]
 s=re.sub(r'<title>.*?</title>',f'<title>{"Luma Onboarding Pilot" if case=="direct" else "Relay Architecture Pilot"}</title>',s)
 (out/'template.html').write_text(s)
 (root/'outputs'/case/'brief.json').write_text(json.dumps(brief,indent=2)+'\n')
print('Built two eight-slide smoke fixtures with all slide text replaced; design CSS and navigation preserved.')
