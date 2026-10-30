(() => {
  const canvas = document.querySelector('.hero-shrimps');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  const frame = canvas.closest('.hero-visual');
  let elapsed = 0, last = null, lastPaint = 0, captionInset = 64;

  const resize = () => {
    const pixelSize = frame.clientWidth < 450 ? 1.5 : 2;
    canvas.width = Math.ceil(frame.clientWidth / pixelSize);
    canvas.height = Math.ceil(frame.clientHeight / pixelSize);
    const caption = frame.querySelector('figcaption');
    if (caption) captionInset = Math.ceil((frame.clientHeight - caption.offsetTop + 12) / pixelSize);
    ctx.imageSmoothingEnabled = false;
  };
  const pixel = (x, y, w, h, color) => {
    ctx.fillStyle = color;
    ctx.fillRect(Math.round(x), Math.round(y), w, h);
  };
  const line = (ax, ay, bx, by, color) => {
    ax=Math.round(ax);ay=Math.round(ay);bx=Math.round(bx);by=Math.round(by);
    const dx=Math.abs(bx-ax),dy=-Math.abs(by-ay),sx=ax<bx?1:-1,sy=ay<by?1:-1;
    let error=dx+dy;
    while(true){pixel(ax,ay,1,1,color);if(ax===bx&&ay===by)break;const e=2*error;if(e>=dy){error+=dy;ax+=sx}if(e<=dx){error+=dx;ay+=sy}}
  };

  function shrimp(x, y, direction, time, pale = false) {
    const shell=pale?'#aebeb0':'#d69b84';
    const shade=pale?'#718f88':'#9e6d62';
    const glint=pale?'#d2dfcd':'#f0c5a7';
    ctx.save();ctx.translate(Math.round(x),Math.round(y));ctx.scale(direction,1);
    // Curved, segmented abdomen, with a small fan at the tail.
    pixel(0,10,4,3,shade);pixel(1,13,4,2,shell);pixel(3,8,3,5,shell);
    pixel(5,6,4,7,shell);pixel(9,4,4,8,shell);pixel(13,3,5,8,shell);
    pixel(18,4,7,7,shell);pixel(22,7,5,5,shell);
    pixel(5,6,3,2,glint);pixel(9,4,3,2,glint);pixel(14,3,4,2,glint);pixel(19,4,5,2,glint);
    line(8,7,8,12,shade);line(12,5,12,11,shade);line(17,5,17,11,shade);line(21,7,21,12,shade);
    // Slow alternating leg steps are only a few pixels long.
    for(let i=0;i<4;i++){
      const step=Math.sin(time*3.5+i*1.8);
      const lx=10+i*4;
      line(lx,11,lx-2,14,shade);line(lx-2,14,lx-4+step*2,17-Math.max(0,step)*2,shell);
    }
    pixel(24,3,2,4,shade);pixel(24,3,2,2,'#263d41');pixel(25,3,1,1,glint);
    const antenna=Math.round(Math.sin(time*.9)*1.5);
    line(26,6,31,2+antenna,shell);line(31,2+antenna,37,3+antenna,shell);
    line(25,8,31,7-antenna,shade);line(31,7-antenna,36,9-antenna,shade);
    // A tiny articulated metal forelimb ends in two mechanical fingers.
    line(25,11,29,13,'#719c9f');line(29,13,33,11,'#c4d8d1');
    pixel(28,12,2,2,'#456d77');pixel(32,10,3,3,'#456d77');
    const gap=Math.sin(time*.65)>0?3:2;
    line(34,11,37,11-gap,'#b9d4cf');line(34,12,37,12+gap,'#b9d4cf');
    line(37,11-gap,39,12-gap,'#e4e5cf');line(37,12+gap,39,11+gap,'#e4e5cf');
    ctx.restore();
  }

  function draw() {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    const w=canvas.width,h=canvas.height;
    const first=elapsed/34;
    const second=elapsed/47+.34;
    const firstTravel=(1-Math.cos(first*Math.PI*2))/2;
    const secondTravel=(1-Math.cos(second*Math.PI*2))/2;
    const left=12+firstTravel*Math.max(10,w*.42-50);
    const right=w-14-secondTravel*Math.max(10,w*.24-30);
    shrimp(left+(Math.sin(first*Math.PI*2)<0?39:0),h-captionInset-18,Math.sin(first*Math.PI*2)<0?-1:1,elapsed);
    shrimp(right-(Math.sin(second*Math.PI*2)<0?39:0),h-captionInset-43,Math.sin(second*Math.PI*2)<0?1:-1,elapsed+2,true);
  }
  function tick(now) {
    if(last!==null)elapsed+=Math.min((now-last)/1000,.1);
    last=now;
    if(now-lastPaint>1000/24){draw();lastPaint=now}
    requestAnimationFrame(tick);
  }
  if('ResizeObserver' in window)new ResizeObserver(resize).observe(frame);
  else addEventListener('resize',resize);
  resize();draw();requestAnimationFrame(tick);
})();
