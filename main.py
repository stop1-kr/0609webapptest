import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정 (가로로 넓게)
st.set_page_config(page_title="✨이차함수 지렁이 대모험✨", page_icon="🐛", layout="wide")

st.markdown("""
    <style>
    /* 상단 여백 최소화 */
    .block-container {
        padding-top: 1.5rem;
        max-width: 1200px; /* 전체 화면 폭 확장 */
    }
    </style>
""", unsafe_allow_html=True)

st.title("🐛 ✨ 이차함수 지렁이 대모험! ✨ 🐛")
st.markdown("**목표:** 그래프 $y = a(x-p)^2 + q$ 를 보고, **a ➔ p ➔ q** 숫자를 순서대로 맞추세요! (방향키로 천천히 이동, 🚀부스트로 빠르게!)")

# 🎮 완벽하게 수정된 HTML/JS 게임 엔진
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body {
            margin: 0; padding: 0;
            background-color: #f8f9fa;
            font-family: 'Pretendard', sans-serif;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            touch-action: none; /* 아이패드 스크롤, 확대 완벽 방지 */
            user-select: none;
            -webkit-user-select: none;
        }
        .container {
            display: flex;
            flex-direction: row;
            gap: 30px;
            background: white;
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        /* 왼쪽: 게임 화면 (크기 키움) */
        .game-panel {
            position: relative;
        }
        #gameCanvas {
            background-color: #1a1a2e;
            border-radius: 15px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
            border: 4px solid #4a4e69;
        }
        /* 오른쪽: 그래프 & 컨트롤러 (크기 키움) */
        .right-panel {
            display: flex;
            flex-direction: column;
            gap: 15px;
            width: 380px;
        }
        .graph-panel {
            background: white;
            border: 3px solid #dee2e6;
            border-radius: 15px;
            padding: 10px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        #graphCanvas {
            background-color: #ffffff;
            border-radius: 10px;
        }
        .status-box {
            background: #ffe3e3;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 1.3rem;
            font-weight: bold;
            color: #d90429;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            animation: pulse 1.5s infinite;
        }
        /* 십자 방향키(D-pad) 레이아웃 */
        .dpad-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 10px;
            margin-top: 5px;
        }
        .dpad-row {
            display: flex;
            gap: 10px;
            justify-content: center;
        }
        .btn {
            background: #457b9d;
            border: none;
            border-radius: 15px;
            color: white;
            font-size: 2.2rem;
            width: 75px;
            height: 75px;
            box-shadow: 0 6px 0 #1d3557;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            touch-action: manipulation;
        }
        .btn:active {
            transform: translateY(6px);
            box-shadow: 0 0 0 #1d3557;
            background: #1d3557;
        }
        /* 부스트 버튼 */
        .boost-btn {
            background: #fca311;
            border: none;
            border-radius: 15px;
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
            padding: 15px;
            width: 100%;
            box-shadow: 0 6px 0 #d08c00;
            cursor: pointer;
            margin-top: 10px;
            transition: all 0.2s;
        }
        .boost-btn.active {
            background: #d90429;
            box-shadow: 0 6px 0 #9d021d;
        }
        .boost-btn:active {
            transform: translateY(6px);
            box-shadow: 0 0 0 transparent;
        }
        
        /* 오버레이 (시작/종료) */
        .overlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.75);
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            z-index: 10;
        }
        .overlay h1 { font-size: 3rem; margin-bottom: 10px; text-shadow: 2px 2px 4px #000; }
        .overlay p { font-size: 1.5rem; margin-bottom: 30px; text-align: center; }
        .start-btn {
            padding: 15px 40px;
            font-size: 1.8rem;
            font-weight: bold;
            border: none;
            border-radius: 40px;
            background: #e63946;
            color: white;
            cursor: pointer;
            box-shadow: 0 6px 15px rgba(230, 57, 70, 0.5);
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.03); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>

<div class="container">
    <!-- 왼쪽: 게임 캔버스 (500x500으로 확대) -->
    <div class="game-panel">
        <canvas id="gameCanvas" width="500" height="500"></canvas>
        <div id="overlay" class="overlay">
            <h1 id="overTitle">🐍 지렁이 대모험</h1>
            <p id="overDesc">그래프를 보고<br>a, p, q를 찾아 지렁이를 키우세요!</p>
            <button id="startBtn" class="start-btn">게임 시작 🚀</button>
        </div>
    </div>

    <!-- 오른쪽: 그래프 및 컨트롤 -->
    <div class="right-panel">
        <div class="graph-panel">
            <h3 style="margin: 5px 0; color:#343a40;">y = a(x-p)² + q</h3>
            <canvas id="graphCanvas" width="360" height="360"></canvas>
        </div>
        
        <div class="status-box" id="targetBox">
            🔥 현재 목표: <span id="targetVar" style="font-size:1.8rem;">a</span> 찾기!
        </div>
        
        <!-- 아이패드 터치용 십자 D패드 및 부스트 -->
        <div class="dpad-container">
            <div class="dpad-row">
                <button class="btn up" id="btnUp">🔼</button>
            </div>
            <div class="dpad-row">
                <button class="btn left" id="btnLeft">◀️</button>
                <button class="btn down" id="btnDown">🔽</button>
                <button class="btn right" id="btnRight">▶️</button>
            </div>
            
            <!-- 부스트 버튼 -->
            <button class="boost-btn" id="btnBoost">🐢 현재 속도: 느림 (터치시 부스트!)</button>
        </div>
        
        <div style="text-align:center; font-weight:bold; color:#457b9d; font-size:1.2rem; margin-top:5px;">
            지렁이 길이: <span id="score">3</span> 🐛
        </div>
    </div>
</div>

<script>
    // === 캔버스 설정 ===
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const graphCanvas = document.getElementById("graphCanvas");
    const graphCtx = graphCanvas.getContext("2d");
    
    const gridSize = 25; // 칸 크기를 25로 키움 (20x20 칸)
    const tileCount = canvas.width / gridSize;
    
    // === 게임 상태 변수 ===
    let snake = [];
    let dx = 0; let dy = 0;
    let nextDx = 0; let nextDy = 0;
    
    let score = 3;
    let gameLoop;
    let isGameOver = true;
    
    // 속도 조절 (부스트 기능)
    const SLOW_SPEED = 500;  // 천천히 (0.5초)
    const FAST_SPEED = 120;  // 빠르게 (0.12초)
    let currentSpeed = SLOW_SPEED;
    let isBoost = false;
    
    // 이차함수 관련 변수
    let currentA, currentP, currentQ;
    let targetStage = 0; // 0:a, 1:p, 2:q
    const stages = ['a', 'p', 'q'];
    let foods = [];

    // === 이차함수 문제 생성 (그래프 눈금 3단위에 맞게 출제) ===
    function generateProblem() {
        // a는 -2, -1, 1, 2 중 하나 (너무 뾰족하거나 퍼지지 않게)
        const aPool = [-2, -1, 1, 2];
        currentA = aPool[Math.floor(Math.random() * aPool.length)];
        
        // p, q는 -6 ~ 6 범위 (3의 배수 위치를 활용하도록)
        currentP = Math.floor(Math.random() * 13) - 6;
        currentQ = Math.floor(Math.random() * 13) - 6;
        
        targetStage = 0;
        document.getElementById("targetVar").innerText = stages[targetStage];
        drawMathGraph();
        spawnFoods();
    }

    // === 좌표평면 그래프 그리기 (3단위 숫자 표시 포함) ===
    function drawMathGraph() {
        const w = graphCanvas.width;
        const h = graphCanvas.height;
        const limit = 10; // -10 ~ 10 까지 표시
        const scale = w / (limit * 2); 
        
        graphCtx.clearRect(0, 0, w, h);
        
        // 그리드 옅게 그리기
        graphCtx.lineWidth = 1;
        for(let i = -limit; i <= limit; i++) {
            // 3단위 선은 조금 더 진하게
            graphCtx.strokeStyle = (i % 3 === 0) ? "#ced4da" : "#f1f3f5";
            
            let px = w/2 + i*scale;
            let py = h/2 - i*scale;
            
            // 세로선
            graphCtx.beginPath(); graphCtx.moveTo(px, 0); graphCtx.lineTo(px, h); graphCtx.stroke();
            // 가로선
            graphCtx.beginPath(); graphCtx.moveTo(0, py); graphCtx.lineTo(w, py); graphCtx.stroke();
        }
        
        // X, Y 메인 축 (진하게)
        graphCtx.strokeStyle = "#495057";
        graphCtx.lineWidth = 2;
        graphCtx.beginPath();
        graphCtx.moveTo(0, h/2); graphCtx.lineTo(w, h/2); // X축
        graphCtx.moveTo(w/2, 0); graphCtx.lineTo(w/2, h); // Y축
        graphCtx.stroke();

        // 눈금 숫자 쓰기 (3단위)
        graphCtx.fillStyle = "#212529";
        graphCtx.font = "bold 13px Arial";
        graphCtx.textAlign = "center";
        graphCtx.textBaseline = "middle";
        
        for(let i = -limit; i <= limit; i++) {
            if(i !== 0 && i % 3 === 0) {
                // X축 숫자
                graphCtx.fillText(i, w/2 + i*scale, h/2 + 15);
                // Y축 숫자
                graphCtx.fillText(i, w/2 - 15, h/2 - i*scale);
            }
        }
        // 원점
        graphCtx.fillText("0", w/2 - 12, h/2 + 15);
        
        // 포물선 그리기
        graphCtx.strokeStyle = "#e63946";
        graphCtx.lineWidth = 4;
        graphCtx.beginPath();
        for(let px = 0; px <= w; px += 2) {
            let mathX = (px - w/2) / scale;
            let mathY = currentA * Math.pow(mathX - currentP, 2) + currentQ;
            let py = h/2 - mathY * scale;
            if(px === 0) graphCtx.moveTo(px, py);
            else graphCtx.lineTo(px, py);
        }
        graphCtx.stroke();
    }

    // === 숫자 블록 생성 ===
    function spawnFoods() {
        foods = [];
        let correctVal = (targetStage === 0) ? currentA : (targetStage === 1) ? currentP : currentQ;
        
        // 오답 만들기
        let wrong1, wrong2;
        do { wrong1 = Math.floor(Math.random() * 13) - 6; } while(wrong1 === correctVal);
        do { wrong2 = Math.floor(Math.random() * 13) - 6; } while(wrong2 === correctVal || wrong2 === wrong1);
        
        const vals = [
            {val: correctVal, isCorrect: true},
            {val: wrong1, isCorrect: false},
            {val: wrong2, isCorrect: false}
        ];
        
        vals.forEach(item => {
            let fx, fy, occupied;
            do {
                occupied = false;
                // 벽에 너무 붙지 않게 (1 ~ tileCount-2) 범위로 스폰
                fx = Math.floor(Math.random() * (tileCount - 2)) + 1;
                fy = Math.floor(Math.random() * (tileCount - 2)) + 1;
                for(let s of snake) if(s.x === fx && s.y === fy) occupied = true;
                for(let f of foods) if(f.x === fx && f.y === fy) occupied = true;
            } while(occupied);
            foods.push({x: fx, y: fy, val: item.val, isCorrect: item.isCorrect});
        });
    }

    // === 게임 로직 ===
    function resetGame() {
        snake = [ {x: 10, y: 10}, {x: 10, y: 11}, {x: 10, y: 12} ];
        score = 3; document.getElementById("score").innerText = score;
        dx = 0; dy = -1; nextDx = 0; nextDy = -1;
        isBoost = false; currentSpeed = SLOW_SPEED;
        updateBoostBtnUI();
        
        generateProblem();
        isGameOver = false;
        document.getElementById("overlay").style.display = "none";
        
        startGameLoop();
    }

    function startGameLoop() {
        if(gameLoop) clearInterval(gameLoop);
        gameLoop = setInterval(updateGame, currentSpeed);
    }

    function updateGame() {
        if(isGameOver) return;
        dx = nextDx; dy = nextDy;
        
        let head = {x: snake[0].x + dx, y: snake[0].y + dy};
        
        // 벽 충돌
        if(head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
            endGame("앗! 벽에 부딪혔어요! 💥"); return;
        }
        // 꼬리 충돌
        for(let i=0; i<snake.length; i++) {
            if(head.x === snake[i].x && head.y === snake[i].y) {
                endGame("앗! 자기 꼬리를 물었어요! 😵"); return;
            }
        }
        
        snake.unshift(head);
        
        // 먹이 체크
        let ate = foods.findIndex(f => f.x === head.x && f.y === head.y);
        if(ate !== -1) {
            if(foods[ate].isCorrect) {
                score++; document.getElementById("score").innerText = score;
                targetStage++;
                if(targetStage > 2) { generateProblem(); } 
                else { 
                    document.getElementById("targetVar").innerText = stages[targetStage];
                    spawnFoods(); 
                }
            } else {
                endGame(`오답입니다! 숫자 ${foods[ate].val} 을(를) 먹었습니다 😭`); return;
            }
        } else {
            snake.pop(); // 먹이 안먹었으면 꼬리 제거
        }
        
        drawGame();
    }

    // === 게임 렌더링 ===
    function drawGame() {
        ctx.fillStyle = "#1a1a2e"; ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.strokeStyle = "#27293d"; ctx.lineWidth = 1;
        for(let i=0; i<tileCount; i++) {
            ctx.beginPath();
            ctx.moveTo(i*gridSize, 0); ctx.lineTo(i*gridSize, canvas.height);
            ctx.moveTo(0, i*gridSize); ctx.lineTo(canvas.width, i*gridSize);
            ctx.stroke();
        }

        foods.forEach(f => {
            ctx.fillStyle = "#ffb703"; ctx.beginPath();
            ctx.arc(f.x*gridSize + gridSize/2, f.y*gridSize + gridSize/2, gridSize/2 - 2, 0, Math.PI*2);
            ctx.fill();
            ctx.fillStyle = "#023047"; ctx.font = "bold 16px Arial";
            ctx.textAlign = "center"; ctx.textBaseline = "middle";
            ctx.fillText(f.val, f.x*gridSize + gridSize/2, f.y*gridSize + gridSize/2);
        });
        
        for(let i=0; i<snake.length; i++) {
            let s = snake[i];
            if(i === 0) {
                ctx.fillStyle = "#06d6a0";
                ctx.fillRect(s.x*gridSize, s.y*gridSize, gridSize-1, gridSize-1);
                ctx.fillStyle = "white";
                ctx.fillRect(s.x*gridSize + 4, s.y*gridSize + 4, 5, 5);
                ctx.fillRect(s.x*gridSize + 15, s.y*gridSize + 4, 5, 5);
            } else {
                ctx.fillStyle = `rgb(6, ${Math.max(100, 214 - i*4)}, 160)`;
                ctx.fillRect(s.x*gridSize+1, s.y*gridSize+1, gridSize-3, gridSize-3);
            }
        }
    }

    function endGame(msg) {
        isGameOver = true; clearInterval(gameLoop);
        document.getElementById("overTitle").innerText = "게임 오버! 💀";
        document.getElementById("overDesc").innerHTML = `${msg}<br><br>최종 길이: <b>${score}</b> 🐛`;
        document.getElementById("startBtn").innerText = "다시 도전하기 🔄";
        document.getElementById("overlay").style.display = "flex";
    }

    // === 조작부 (이벤트 버그 수정) ===
    function changeDir(newDx, newDy) {
        // 좌우 이동 중일 때는 상하 입력만 허용
        if (dx !== 0 && newDy !== 0) { nextDx = 0; nextDy = newDy; }
        // 상하 이동 중일 때는 좌우 입력만 허용
        if (dy !== 0 && newDx !== 0) { nextDx = newDx; nextDy = 0; }
        // 멈춰있을 때 (시작 전)
        if (dx === 0 && dy === 0) { nextDx = newDx; nextDy = newDy; }
    }

    // 아이패드 지원 확실한 pointerdown 사용 (mousedown, touchstart 모두 커버)
    const bindBtn = (id, ndx, ndy) => {
        document.getElementById(id).addEventListener("pointerdown", (e) => { 
            e.preventDefault(); 
            changeDir(ndx, ndy); 
        });
    };
    bindBtn("btnUp", 0, -1); bindBtn("btnDown", 0, 1);
    bindBtn("btnLeft", -1, 0); bindBtn("btnRight", 1, 0);

    // 부스트(속도업) 버튼 토글 로직
    const btnBoost = document.getElementById("btnBoost");
    function updateBoostBtnUI() {
        if(isBoost) {
            btnBoost.classList.add("active");
            btnBoost.innerText = "🚀 부스트 ON! (빨라짐)";
        } else {
            btnBoost.classList.remove("active");
            btnBoost.innerText = "🐢 현재 속도: 느림 (터치시 부스트!)";
        }
    }
    
    btnBoost.addEventListener("pointerdown", (e) => {
        e.preventDefault();
        if(isGameOver) return;
        isBoost = !isBoost;
        currentSpeed = isBoost ? FAST_SPEED : SLOW_SPEED;
        updateBoostBtnUI();
        startGameLoop(); // 속도 즉시 반영
    });

    // 시작 버튼
    document.getElementById("startBtn").addEventListener("pointerdown", (e) => { 
        e.preventDefault(); 
        resetGame(); 
    });

    drawMathGraph(); // 초기 빈 화면 출력
</script>
</body>
</html>
"""

# HTML 렌더링 (가로 세로 넉넉하게 지정하여 스크롤 생김 방지)
components.html(game_html, height=750)

st.write("---")
st.markdown("### 💡 게임 플레이 팁")
st.markdown("""
* **느긋하게 생각하세요!** 지렁이는 아주 천천히 움직입니다. 좌표평면의 **3단위 눈금**을 참고하여 꼭짓점 좌표와 그래프의 폭(a)을 계산할 시간이 충분합니다.
* **부스트 활용하기:** 정답을 찾았다면 `부스트` 버튼을 눌러 빠르게 정답 블록을 먹어 치우세요! 다시 누르면 원래 속도로 돌아옵니다.
* **이동 규칙:** 지렁이는 좌우로 이동 중일 때는 위/아래 방향키만, 위아래로 이동 중일 때는 좌/우 방향키만 먹힙니다. 벽과 꼬리에 조심하세요!
""")
