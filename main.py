import streamlit as st
import streamlit.components.v1 as components

# 페이지 기본 설정 (가로로 넓게 써야 아이패드에서 왼쪽/오른쪽 배치가 예쁩니다)
st.set_page_config(page_title="✨이차함수 지렁이 대모험✨", page_icon="🐛", layout="wide")

st.markdown("""
    <style>
    /* 상단 여백 최소화 */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🐛 ✨ 이차함수 지렁이 대모험! ✨ 🐛")
st.markdown("**목표:** 우측의 그래프 $y = a(x-p)^2 + q$ 를 보고, 알맞은 **a ➔ p ➔ q** 숫자를 순서대로 먹어 지렁이를 키워보세요! (아이패드 터치 지원 🎮)")

# 🎮 게임의 핵심이 되는 HTML/CSS/JS 코드 (외부 라이브러리 X)
game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body {
            margin: 0; padding: 0;
            background-color: #f0f8ff;
            font-family: 'Comic Sans MS', 'Pretendard', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            touch-action: none; /* 아이패드 스크롤 방지 */
            user-select: none;
        }
        .container {
            display: flex;
            flex-direction: row;
            gap: 20px;
            background: white;
            padding: 20px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        /* 왼쪽: 게임 화면 */
        .game-panel {
            position: relative;
        }
        #gameCanvas {
            background-color: #1a1a2e;
            border-radius: 15px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
            border: 4px solid #4a4e69;
        }
        /* 오른쪽: 그래프 & 컨트롤러 */
        .right-panel {
            display: flex;
            flex-direction: column;
            gap: 15px;
            width: 300px;
        }
        .graph-panel {
            background: white;
            border: 3px dashed #9a8c98;
            border-radius: 15px;
            padding: 10px;
            text-align: center;
        }
        #graphCanvas {
            background-color: #fdfdfd;
            border-radius: 10px;
        }
        .status-box {
            background: #ffe3e3;
            padding: 10px;
            border-radius: 10px;
            text-align: center;
            font-size: 1.2rem;
            font-weight: bold;
            color: #d90429;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            animation: pulse 1.5s infinite;
        }
        /* 조이패드 (D-pad) */
        .dpad {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            grid-template-rows: 1fr 1fr 1fr;
            gap: 5px;
            margin-top: 10px;
            width: 240px;
            height: 240px;
            align-self: center;
        }
        .btn {
            background: linear-gradient(145deg, #a8dadc, #457b9d);
            border: none;
            border-radius: 15px;
            color: white;
            font-size: 2rem;
            box-shadow: 0 8px 15px rgba(0,0,0,0.2);
            cursor: pointer;
        }
        .btn:active {
            transform: scale(0.95);
            background: #1d3557;
        }
        .btn.up { grid-column: 2; grid-row: 1; }
        .btn.left { grid-column: 1; grid-row: 2; }
        .btn.right { grid-column: 3; grid-row: 2; }
        .btn.down { grid-column: 2; grid-row: 3; }
        
        /* 오버레이 (시작/종료) */
        .overlay {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.7);
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            z-index: 10;
        }
        .overlay h1 { font-size: 2.5rem; margin-bottom: 10px; text-shadow: 2px 2px 4px #000; }
        .overlay p { font-size: 1.5rem; margin-bottom: 20px; }
        .start-btn {
            padding: 15px 30px;
            font-size: 1.5rem;
            font-weight: bold;
            border: none;
            border-radius: 30px;
            background: #e63946;
            color: white;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(230, 57, 70, 0.5);
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>

<div class="container">
    <!-- 왼쪽: 게임 캔버스 -->
    <div class="game-panel">
        <canvas id="gameCanvas" width="400" height="400"></canvas>
        <div id="overlay" class="overlay">
            <h1 id="overTitle">🐍 지렁이 대모험</h1>
            <p id="overDesc">그래프를 보고 a, p, q를 맞춰보세요!</p>
            <button id="startBtn" class="start-btn">게임 시작 🚀</button>
        </div>
    </div>

    <!-- 오른쪽: 그래프 및 컨트롤 -->
    <div class="right-panel">
        <div class="graph-panel">
            <h3 style="margin: 5px 0;">y = a(x-p)² + q</h3>
            <canvas id="graphCanvas" width="280" height="280"></canvas>
        </div>
        <div class="status-box" id="targetBox">
            🔥 현재 목표: <span id="targetVar" style="font-size:1.5rem;">a</span> 찾기!
        </div>
        <div style="text-align:center; font-weight:bold; color:#457b9d; font-size:1.2rem;">
            현재 길이: <span id="score">3</span> 🐛
        </div>
        
        <!-- 아이패드 터치용 D패드 -->
        <div class="dpad">
            <button class="btn up" id="btnUp">🔼</button>
            <button class="btn left" id="btnLeft">◀️</button>
            <button class="btn right" id="btnRight">▶️</button>
            <button class="btn down" id="btnDown">🔽</button>
        </div>
    </div>
</div>

<script>
    // === 게임 기본 설정 ===
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    const graphCanvas = document.getElementById("graphCanvas");
    const graphCtx = graphCanvas.getContext("2d");
    
    const gridSize = 20;
    const tileCount = canvas.width / gridSize;
    
    let snake = [];
    let dx = 0; let dy = 0;
    let nextDx = 0; let nextDy = 0; // 빠른 키입력 오류 방지용
    
    let score = 3;
    let gameLoop;
    let isGameOver = true;
    
    // 이차함수 관련 변수
    let currentA, currentP, currentQ;
    let targetStage = 0; // 0: a찾기, 1: p찾기, 2: q찾기
    const stages = ['a', 'p', 'q'];
    let foods = []; // 화면에 떠있는 숫자 블록들 [{x, y, val, isCorrect}]

    // HTML 요소
    const overlay = document.getElementById("overlay");
    const overTitle = document.getElementById("overTitle");
    const overDesc = document.getElementById("overDesc");
    const startBtn = document.getElementById("startBtn");
    const targetVarSpan = document.getElementById("targetVar");
    const scoreSpan = document.getElementById("score");

    // === 이차함수 문제 생성기 ===
    function generateProblem() {
        // a는 0이 아닌 -3 ~ 3
        do { currentA = Math.floor(Math.random() * 7) - 3; } while(currentA === 0);
        // p, q는 -4 ~ 4
        currentP = Math.floor(Math.random() * 9) - 4;
        currentQ = Math.floor(Math.random() * 9) - 4;
        
        targetStage = 0;
        updateTargetUI();
        drawMathGraph();
        spawnFoods();
    }

    // === 그래프 그리기 ===
    function drawMathGraph() {
        const w = graphCanvas.width;
        const h = graphCanvas.height;
        const scale = w / 14; // x, y축 -7 ~ 7 정도 보여주기
        
        graphCtx.clearRect(0, 0, w, h);
        
        // 그리드 그리기
        graphCtx.strokeStyle = "#e9ecef";
        graphCtx.lineWidth = 1;
        for(let i = -7; i <= 7; i++) {
            graphCtx.beginPath();
            graphCtx.moveTo(0, h/2 - i*scale); graphCtx.lineTo(w, h/2 - i*scale);
            graphCtx.moveTo(w/2 + i*scale, 0); graphCtx.lineTo(w/2 + i*scale, h);
            graphCtx.stroke();
        }
        
        // x, y 축
        graphCtx.strokeStyle = "#adb5bd";
        graphCtx.lineWidth = 2;
        graphCtx.beginPath();
        graphCtx.moveTo(0, h/2); graphCtx.lineTo(w, h/2); // x축
        graphCtx.moveTo(w/2, 0); graphCtx.lineTo(w/2, h); // y축
        graphCtx.stroke();
        
        // 포물선 그리기
        graphCtx.strokeStyle = "#e63946";
        graphCtx.lineWidth = 3;
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

    // === UI 업데이트 ===
    function updateTargetUI() {
        targetVarSpan.innerText = stages[targetStage];
        scoreSpan.innerText = score;
    }

    // === 숫자 블록(먹이) 생성 ===
    function spawnFoods() {
        foods = [];
        let correctVal = (targetStage === 0) ? currentA : (targetStage === 1) ? currentP : currentQ;
        
        // 오답 2개 생성
        let wrong1, wrong2;
        do { wrong1 = Math.floor(Math.random() * 9) - 4; } while(wrong1 === correctVal);
        do { wrong2 = Math.floor(Math.random() * 9) - 4; } while(wrong2 === correctVal || wrong2 === wrong1);
        
        const valsToSpawn = [
            {val: correctVal, isCorrect: true},
            {val: wrong1, isCorrect: false},
            {val: wrong2, isCorrect: false}
        ];
        
        // 랜덤 위치 배정
        valsToSpawn.forEach(item => {
            let fx, fy;
            let occupied;
            do {
                occupied = false;
                fx = Math.floor(Math.random() * tileCount);
                fy = Math.floor(Math.random() * tileCount);
                // 뱀 위치와 겹치는지
                for(let s of snake) { if(s.x === fx && s.y === fy) occupied = true; }
                // 다른 먹이와 겹치는지
                for(let f of foods) { if(f.x === fx && f.y === fy) occupied = true; }
            } while(occupied);
            
            foods.push({x: fx, y: fy, val: item.val, isCorrect: item.isCorrect});
        });
    }

    // === 게임 초기화 및 시작 ===
    function resetGame() {
        snake = [
            {x: 10, y: 10},
            {x: 10, y: 11},
            {x: 10, y: 12}
        ];
        score = 3;
        dx = 0; dy = -1;
        nextDx = 0; nextDy = -1;
        
        generateProblem();
        isGameOver = false;
        overlay.style.display = "none";
        
        if(gameLoop) clearInterval(gameLoop);
        gameLoop = setInterval(updateGame, 150); // 속도 (150ms)
    }

    // === 메인 게임 루프 ===
    function updateGame() {
        if(isGameOver) return;
        
        dx = nextDx;
        dy = nextDy;
        
        // 머리 이동
        let head = {x: snake[0].x + dx, y: snake[0].y + dy};
        
        // 1. 벽 충돌 체크
        if(head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
            endGame("앗! 벽에 부딪혔어요! 💥");
            return;
        }
        
        // 2. 자기 몸 충돌 체크
        for(let i=0; i<snake.length; i++) {
            if(head.x === snake[i].x && head.y === snake[i].y) {
                endGame("앗! 자기 꼬리를 물었어요! 😵");
                return;
            }
        }
        
        snake.unshift(head); // 머리 추가
        
        // 3. 먹이 먹음 체크
        let ateFoodIndex = -1;
        for(let i=0; i<foods.length; i++) {
            if(head.x === foods[i].x && head.y === foods[i].y) {
                ateFoodIndex = i;
                break;
            }
        }
        
        if(ateFoodIndex !== -1) {
            let eaten = foods[ateFoodIndex];
            if(eaten.isCorrect) {
                // 정답!
                score++;
                targetStage++;
                if(targetStage > 2) {
                    // 한 문제 완료 (a,p,q 모두 찾음)
                    generateProblem();
                } else {
                    updateTargetUI();
                    spawnFoods();
                }
            } else {
                // 오답!
                endGame(`틀렸어요! 정답이 아닌 숫자 ${eaten.val} 를 먹었습니다! 😭`);
                return;
            }
        } else {
            snake.pop(); // 먹이를 안먹었으면 꼬리 자르기
        }
        
        drawGame();
    }

    // === 게임 화면 그리기 ===
    function drawGame() {
        // 배경
        ctx.fillStyle = "#1a1a2e";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // 그리드 (선택사항)
        ctx.strokeStyle = "#27293d";
        for(let i=0; i<tileCount; i++) {
            ctx.beginPath();
            ctx.moveTo(i*gridSize, 0); ctx.lineTo(i*gridSize, canvas.height);
            ctx.moveTo(0, i*gridSize); ctx.lineTo(canvas.width, i*gridSize);
            ctx.stroke();
        }

        // 먹이(숫자 블록) 그리기
        foods.forEach(f => {
            // 귀여운 동그라미 블록
            ctx.fillStyle = "#ffb703";
            ctx.beginPath();
            ctx.arc(f.x*gridSize + gridSize/2, f.y*gridSize + gridSize/2, gridSize/2 - 2, 0, Math.PI*2);
            ctx.fill();
            
            // 숫자 텍스트
            ctx.fillStyle = "#023047";
            ctx.font = "bold 14px Arial";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(f.val, f.x*gridSize + gridSize/2, f.y*gridSize + gridSize/2);
        });
        
        // 지렁이 그리기
        for(let i=0; i<snake.length; i++) {
            let s = snake[i];
            
            if(i === 0) {
                // 머리 (네온 그린)
                ctx.fillStyle = "#06d6a0";
                ctx.fillRect(s.x*gridSize, s.y*gridSize, gridSize-1, gridSize-1);
                // 눈 그리기
                ctx.fillStyle = "white";
                ctx.fillRect(s.x*gridSize + 3, s.y*gridSize + 3, 4, 4);
                ctx.fillRect(s.x*gridSize + 12, s.y*gridSize + 3, 4, 4);
            } else {
                // 꼬리로 갈수록 색상 변화
                let colorVal = Math.max(100, 214 - i*3);
                ctx.fillStyle = `rgb(6, ${colorVal}, 160)`;
                ctx.fillRect(s.x*gridSize+1, s.y*gridSize+1, gridSize-3, gridSize-3);
            }
        }
    }

    // === 게임 오버 처리 ===
    function endGame(msg) {
        isGameOver = true;
        clearInterval(gameLoop);
        
        overTitle.innerText = "게임 오버! 💀";
        overTitle.style.color = "#ff4d4d";
        overDesc.innerHTML = `${msg}<br><br>최종 길이: <b>${score}</b> 🐛`;
        startBtn.innerText = "다시 도전하기 🔄";
        overlay.style.display = "flex";
    }

    // === 조작 이벤트 등록 ===
    function changeDir(newDx, newDy) {
        // 반대 방향으로 즉시 꺾는 것 방지
        if(dy === 0 && newDx !== 0) { nextDx = newDx; nextDy = 0; }
        if(dx === 0 && newDy !== 0) { nextDx = 0; nextDy = newDy; }
    }

    // 아이패드 터치 (D-pad)
    const bindTouch = (id, ndx, ndy) => {
        const btn = document.getElementById(id);
        btn.addEventListener("touchstart", (e) => { e.preventDefault(); changeDir(ndx, ndy); });
        btn.addEventListener("mousedown", (e) => { e.preventDefault(); changeDir(ndx, ndy); }); // PC 마우스 겸용
    };
    bindTouch("btnUp", 0, -1);
    bindTouch("btnDown", 0, 1);
    bindTouch("btnLeft", -1, 0);
    bindTouch("btnRight", 1, 0);

    // 키보드 조작 (PC 디버깅용)
    document.addEventListener("keydown", (e) => {
        if(isGameOver) return;
        switch(e.key) {
            case "ArrowUp": changeDir(0, -1); break;
            case "ArrowDown": changeDir(0, 1); break;
            case "ArrowLeft": changeDir(-1, 0); break;
            case "ArrowRight": changeDir(1, 0); break;
        }
    });

    // 시작 버튼
    startBtn.addEventListener("click", resetGame);
    startBtn.addEventListener("touchstart", (e) => { e.preventDefault(); resetGame(); });

    // 초기 화면 그리기
    drawMathGraph();

</script>
</body>
</html>
"""

# HTML을 Streamlit에 임베딩 (아이패드에서 잘리거나 스크롤 생기지 않도록 높이 넉넉히 지정)
components.html(game_html, height=650)

st.write("---")
st.markdown("### 💡 게임 규칙")
st.markdown("""
1. 화면 우측 상단에 **이차함수 그래프**가 무작위로 그려집니다.
2. 그래프의 모양(볼록한 방향, 폭)과 꼭짓점의 위치를 보고 식 $y=a(x-p)^2+q$ 의 **$a, p, q$ 값**을 암산해보세요.
3. 현재 먹어야 하는 목표(a, p, q 중 하나)가 빨간 박스에 깜빡입니다.
4. 게임 화면(왼쪽)에 나타난 3개의 숫자 블록 중, **정답인 숫자**를 찾아 지렁이를 조종해 먹으세요!
5. **정답을 먹으면:** 지렁이가 길어지고 다음 목표로 넘어갑니다. (a ➔ p ➔ q)
6. **오답을 먹거나 벽/꼬리에 부딪히면:** 게임 오버! 💀
""")
