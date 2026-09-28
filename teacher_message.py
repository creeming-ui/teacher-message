from flask import Flask, request, jsonify, render_template_string, send_file
from pathlib import Path
from datetime import datetime
import json
import os

app = Flask(__name__)
RESPONSES = Path("responses.json")

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>A Small Message 🌸</title>
<style>
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;min-height:100vh;overflow-x:hidden;font-family:Georgia,"Times New Roman",serif;color:#5b3847;background:radial-gradient(circle at 15% 10%,#fff 0%,transparent 30%),linear-gradient(135deg,#fffaff,#ffe8f1,#fff7fb)}
#petals{position:fixed;inset:0;overflow:hidden;pointer-events:none;z-index:0}
.petal{position:absolute;top:-40px;width:15px;height:10px;border-radius:80% 20% 80% 20%;background:linear-gradient(135deg,#ffc4d7,#ed91b1);opacity:.75;filter:drop-shadow(0 2px 3px rgba(180,80,120,.15));animation:fall linear infinite}
@keyframes fall{0%{transform:translate3d(0,-40px,0) rotate(0deg)}25%{transform:translate3d(60px,25vh,0) rotate(100deg)}50%{transform:translate3d(-30px,50vh,0) rotate(220deg)}75%{transform:translate3d(80px,75vh,0) rotate(350deg)}100%{transform:translate3d(-20px,110vh,0) rotate(520deg)}}
.wrapper{min-height:100vh;display:flex;justify-content:center;align-items:center;padding:25px;position:relative;z-index:2}
.card{width:min(720px,95vw);padding:35px 25px;text-align:center;background:rgba(255,255,255,.72);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border:1px solid rgba(238,170,195,.65);border-radius:32px;box-shadow:0 25px 80px rgba(160,70,110,.15);animation:cardIn .8s ease}
@keyframes cardIn{from{opacity:0;transform:translateY(25px) scale(.97)}to{opacity:1;transform:translateY(0) scale(1)}}
.flower{font-size:30px;letter-spacing:5px;margin-bottom:10px}h1{margin:0 0 15px;font-size:clamp(29px,8vw,45px);color:#754358}h2{color:#8f4c69}p{font-size:17px;line-height:1.8}.small{font-size:13px;opacity:.65}
input,textarea{width:100%;padding:15px 17px;margin:10px 0;border-radius:18px;border:1px solid #e6b1c4;background:rgba(255,250,253,.92);color:#593846;font:inherit;outline:none;transition:.25s}
input:focus,textarea:focus{border-color:#d9789f;box-shadow:0 0 0 4px rgba(217,120,159,.1)}textarea{min-height:155px;resize:vertical}
button{border:none;border-radius:999px;padding:14px 26px;margin:8px;font:600 16px Georgia,serif;cursor:pointer;color:white;background:linear-gradient(135deg,#df79a5,#c75c8d);box-shadow:0 9px 22px rgba(200,90,140,.25);transition:transform .25s,box-shadow .25s}
button:hover{transform:translateY(-3px);box-shadow:0 13px 27px rgba(200,90,140,.3)}
.secondary{background:rgba(255,255,255,.95);color:#a04e72;border:1px solid #e3a7bd}
.story,.letter{text-align:left;padding:22px;margin-top:20px;border-radius:23px;background:rgba(255,248,251,.88);border:1px solid rgba(234,170,193,.5);box-shadow:inset 0 1px 0 rgba(255,255,255,.8)}
.letter{background:linear-gradient(145deg,#fffafd,#fff0f6)}.signature{text-align:right;margin-top:25px;font-style:italic;font-size:19px;color:#9b4f70}
.divider{display:flex;align-items:center;gap:10px;margin:20px 0;color:#d07a9c}.divider:before,.divider:after{content:"";height:1px;flex:1;background:#edb3c8}
.hidden{display:none!important}#sent{color:#a14f72;font-weight:bold}
.music{position:fixed;right:18px;bottom:18px;z-index:20;width:54px;height:54px;padding:0;margin:0;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:21px;background:rgba(255,255,255,.8);color:#a04e72;border:1px solid #e3a7bd;backdrop-filter:blur(12px);box-shadow:0 10px 30px rgba(160,70,110,.2)}
.footer{margin-top:35px;padding-top:20px;border-top:1px solid rgba(220,150,175,.35);color:#9b6077;font-size:14px;line-height:1.7;letter-spacing:.5px}.footer strong{font-size:16px;color:#80445d}
@media(max-width:600px){.wrapper{padding:15px}.card{padding:28px 18px;border-radius:25px}p{font-size:16px}button{padding:12px 21px}}
</style>
</head>
<body>
<div id="petals"></div>
<audio id="music" loop preload="none"><source src="/music.mp3" type="audio/mpeg"></audio>
<button class="music" id="musicBtn" onclick="toggleMusic()" aria-label="Music">🎵</button>

<div class="wrapper"><div class="card">

<section id="step1">
<div class="flower">🌸 🌸 🌸</div><h1>Hi Ma'am 🌸</h1><p>How are you?</p>
<input id="how" type="text" placeholder="Write your answer here...">
<button onclick="next1()">Continue 🌷</button>
<p class="small">A small and respectful message from Dev.</p>
</section>

<section id="step2" class="hidden">
<div class="flower">🌸</div><h1>Can I tell you something?</h1>
<p>There is something that happened at school that I wanted to explain honestly.</p><p>I hope you won't be angry with me.</p>
<button id="yesButton" onclick="yesClicked()">YES 😭</button><button class="secondary" onclick="noClicked()">NO 🌸</button>
<p id="hint" class="small"></p>
</section>

<section id="step3" class="hidden">
<div class="flower">🌷</div><h1>Thank you for understanding.</h1>
<p>I'll explain everything from the beginning, because I don't want there to be any misunderstanding.</p>
<button onclick="showRumor()">Continue 🌸</button>
</section>

<section id="rumor" class="hidden">
<div class="flower">🌸</div><h1>What actually happened</h1>
<div class="story">
<h2>It started with Swagat.</h2>
<p>I had asked my classmate, <b>Swagat Barik</b>, for a number because I wanted to contact you about something.</p>
<p>After I asked him, he looked at me for a while and seemed to think that something else was going on.</p>
<p>Later, Swagat started spreading the rumor that <b>“Dev loves Surabhi Ma'am.”</b></p>
<p>And honestly, I want to be truthful about this — <b>yes, I did have feelings for you.</b> I don't want to lie about that part.</p>
<p>But I never wanted those feelings to become a reason for people to disrespect you, tease you, or make the situation uncomfortable.</p>
<p>After Swagat spread the rumor, some of my friends started teasing me repeatedly, and some students also began making disrespectful comments about you.</p>
<p>I genuinely don't support those comments.</p>
<p>That's why I wanted to explain everything myself, honestly and respectfully, instead of letting the rumor tell the whole story.</p>
</div>
<div class="divider">🌸</div><button onclick="showClarification()">Continue 🌷</button>
</section>

<section id="clarification" class="hidden">
<div class="flower">🌸</div><h1>My clarification</h1>
<div class="story">
<p>I wasn't trying to create an awkward situation or make you uncomfortable.</p>
<p>I simply wanted to clear up the rumor and explain my side honestly.</p>
<p>I thought it would be better to tell you the truth instead of letting other people's version become the story you heard.</p>
<p>I'm sorry that this whole situation happened and that you had to be involved in it.</p>
</div><button onclick="showSorry()">Read my sorry letter 💌</button>
</section>

<section id="sorry" class="hidden">
<div class="flower">🌸</div><h1>A Sorry Letter 😔</h1>
<div class="letter">
<p>Dear Ma'am,</p>
<p>I'm really sorry if this whole situation made you uncomfortable or caused any misunderstanding. I never wanted the rumor started by Swagat to create an awkward situation for you.</p>
<p>I just wanted to explain what actually happened and clear things up honestly. I'm also sorry that you had to hear people saying things that weren't true.</p>
<p>I respect you as my teacher, and I don't want this misunderstanding to affect that respect.</p>
<p>I also don't support the disrespectful things some students say because of the rumor.</p>
<p>Thank you for taking the time to read this and understand my side.</p>
<p>I'm genuinely sorry, Ma'am. 😔🌸</p>
<p class="signature">— Dev</p>
</div><button onclick="showReply()">Continue to response 💌</button>
</section>

<section id="reply" class="hidden">
<div class="flower">🌸</div><h1>Your Response 💌</h1>
<p>If you'd like to say anything, you can write it below.</p>
<textarea id="replyText" placeholder="Write your response here..."></textarea>
<button onclick="sendReply()">Send 🌸</button>
<p id="sent" class="hidden">Thank you for reading and responding, Ma'am. 🌷</p>
<p class="small">Please don't include passwords or other private information.</p>
</section>

<div class="footer"><strong>Made With Love</strong><br>Co-powered by KAKTUX &amp; DEV 🌸</div>
</div></div>

<script>
const petals=document.getElementById("petals");
for(let i=0;i<40;i++){const p=document.createElement("div");p.className="petal";p.style.left=Math.random()*100+"%";p.style.animationDuration=(5+Math.random()*9)+"s";p.style.animationDelay=(-Math.random()*12)+"s";p.style.transform="rotate("+Math.random()*360+"deg)";petals.appendChild(p)}
const music=document.getElementById("music"), musicBtn=document.getElementById("musicBtn");let playing=false;
function toggleMusic(){if(!music.src||music.src.endsWith("/music.mp3")){alert("Add your chill MP3 as music.mp3 beside teacher_message.py to enable music. 🌸");return}if(playing){music.pause();musicBtn.textContent="🎵";playing=false}else{music.play().then(()=>{playing=true;musicBtn.textContent="⏸️"}).catch(()=>{})}}
function hide(id){document.getElementById(id).classList.add("hidden")}function show(id){document.getElementById(id).classList.remove("hidden")}
function next1(){const a=document.getElementById("how").value.trim();if(!a){document.getElementById("how").focus();return}hide("step1");show("step2")}
let dodges=0;
function yesClicked(){const b=document.getElementById("yesButton");dodges++;const x=Math.random()*220-110,y=Math.random()*100-50,r=Math.random()*16-8;b.style.transform=`translate(${x}px,${y}px) rotate(${r}deg)`;document.getElementById("hint").textContent=dodges<3?"Hehe 😭 maybe try the other option?":"You can choose NO if you're comfortable 🌸"}
function noClicked(){hide("step2");show("step3")}function showRumor(){hide("step3");show("rumor")}function showClarification(){hide("rumor");show("clarification")}function showSorry(){hide("clarification");show("sorry")}function showReply(){hide("sorry");show("reply")}
async function sendReply(){const m=document.getElementById("replyText").value.trim();if(!m)return;try{const r=await fetch("/respond",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:m})});if(r.ok){document.getElementById("replyText").value="";document.getElementById("sent").classList.remove("hidden")}else alert("The response could not be saved. Please try again.")}catch(e){alert("The response could not be saved. Please try again.")}}
</script>
</body>
</html>
"""

def load_responses():
    if not RESPONSES.exists():
        return []
    try:
        return json.loads(RESPONSES.read_text(encoding="utf-8"))
    except Exception:
        return []

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/music.mp3")
def music():
    music_file = Path("music.mp3")
    if not music_file.exists():
        return ("Music file not added yet.", 404)
    return send_file(music_file, mimetype="audio/mpeg")

@app.post("/respond")
def respond():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"ok": False}), 400
    responses = load_responses()
    responses.append({"time": datetime.now().isoformat(timespec="seconds"), "message": message})
    RESPONSES.write_text(json.dumps(responses, ensure_ascii=False, indent=2), encoding="utf-8")
    return jsonify({"ok": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
