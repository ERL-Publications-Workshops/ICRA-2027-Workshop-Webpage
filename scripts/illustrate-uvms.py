"""Draw the workshop's conceptual UVMS as a self-contained orthographic SVG."""
from math import cos, sin, pi, sqrt
from pathlib import Path

faces = []
VIEW = (.72, .85, .6234)
LIGHT = (-.35, -.45, 1.0)

def add(a, b): return tuple(x+y for x,y in zip(a,b))
def sub(a, b): return tuple(x-y for x,y in zip(a,b))
def scale(a, s): return tuple(x*s for x in a)
def dot(a, b): return sum(x*y for x,y in zip(a,b))
def unit(a): return scale(a, 1/sqrt(dot(a,a)))
def cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def project(p):
    x,y,z=p
    return (365+1.18*(.85*x-.72*y), 355+1.18*(.37*x+.42*y-z))
def color(hex_color, normal):
    light = .67 + .37*max(0,dot(unit(normal),unit(LIGHT))) + .12*max(0,dot(unit(normal),unit(VIEW)))
    rgb=[min(255,round(int(hex_color[i:i+2],16)*light)) for i in (1,3,5)]
    return '#'+''.join(f'{v:02x}' for v in rgb)
def face(points, material, normal, flat=False):
    if dot(normal,VIEW)<-.001:return
    depth=sum(dot(p,VIEW) for p in points)/len(points)
    points_string=' '.join(f'{x:.2f},{y:.2f}' for x,y in map(project,points))
    fill=material if flat else color(material,normal)
    faces.append((depth,f'<polygon points="{points_string}" fill="{fill}" stroke="{fill}" stroke-width=".35"/>'))
def box(lo,hi,material):
    x,y,z=lo;X,Y,Z=hi
    face([(X,y,z),(X,Y,z),(X,Y,Z),(X,y,Z)],material,(1,0,0))
    face([(x,y,z),(x,y,Z),(x,Y,Z),(x,Y,z)],material,(-1,0,0))
    face([(x,Y,z),(x,Y,Z),(X,Y,Z),(X,Y,z)],material,(0,1,0))
    face([(x,y,z),(X,y,z),(X,y,Z),(x,y,Z)],material,(0,-1,0))
    face([(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)],material,(0,0,1))
    face([(x,y,z),(x,Y,z),(X,Y,z),(X,y,z)],material,(0,0,-1))
def basis(axis):
    axis=unit(axis)
    u=unit(cross(axis,(0,0,1) if abs(axis[2])<.9 else (0,1,0)))
    return axis,u,cross(axis,u)
def cylinder(a,b,r,material,cap=None,n=32):
    axis,u,v=basis(sub(b,a))
    ring=[add(scale(u,cos(i*2*pi/n)),scale(v,sin(i*2*pi/n))) for i in range(n)]
    for i in range(n):
        j=(i+1)%n
        face([add(a,scale(ring[i],r)),add(b,scale(ring[i],r)),add(b,scale(ring[j],r)),add(a,scale(ring[j],r))],material,add(ring[i],ring[j]))
    face([add(b,scale(q,r)) for q in ring],cap or material,axis)
    face([add(a,scale(q,r)) for q in reversed(ring)],cap or material,scale(axis,-1))
def ring(a,b,outer,inner,material,rim=None,n=32):
    axis,u,v=basis(sub(b,a))
    radial=[add(scale(u,cos(i*2*pi/n)),scale(v,sin(i*2*pi/n))) for i in range(n)]
    for i in range(n):
        j=(i+1)%n;q,p=radial[i],radial[j]
        face([add(a,scale(q,outer)),add(b,scale(q,outer)),add(b,scale(p,outer)),add(a,scale(p,outer))],material,add(q,p))
        face([add(a,scale(q,inner)),add(b,scale(q,inner)),add(b,scale(p,inner)),add(a,scale(p,inner))],'#182f3e',scale(add(q,p),-1))
        for origin,normal in [(a,scale(axis,-1)),(b,axis)]:
            face([add(origin,scale(q,inner)),add(origin,scale(q,outer)),add(origin,scale(p,outer)),add(origin,scale(p,inner))],rim or material,normal)
def duct(center, direction, radius=27, length=30):
    axis,u,v=basis(direction)
    a=add(center,scale(axis,-length/2));b=add(center,scale(axis,length/2))
    ring(a,b,radius,radius*.76,'#283d4a','#718a91')
    rotor=add(center,scale(axis,length*.30))
    for blade in range(3):
        angle=blade*2*pi/3+.15
        points=[]
        for r,theta in [(3,angle),(radius*.67,angle+.25),(radius*.69,angle+.60),(radius*.38,angle+.84),(3,angle+.9)]:
            points.append(add(rotor,add(scale(u,r*cos(theta)),scale(v,r*sin(theta)))))
        face(points,'#a4c4c2',axis)
        face(list(reversed(points)),'#66878e',scale(axis,-1))
    cylinder(add(rotor,scale(axis,-2)),add(rotor,scale(axis,4)),5,'#759497','#d0d9cd',16)
def float_module(y):
    # The narrow, chamfered buoyancy modules leave the pressure tube visible.
    outline=[(-126,y-17),(-114,y-25),(112,y-25),(126,y-17),(126,y+17),(114,y+25),(-114,y+25),(-126,y+17)]
    top=[(x*.97,y+(yy-y)*.82,148) for x,yy in outline]
    lower=[(x,yy,124) for x,yy in outline]
    shoulder=[(x,yy,140) for x,yy in outline]
    for i in range(8):
        j=(i+1)%8
        dx=outline[j][0]-outline[i][0];dy=outline[j][1]-outline[i][1]
        normal=(dy,-dx,0)
        face([lower[i],lower[j],shoulder[j],shoulder[i]],'#1981bd',normal)
        face([shoulder[i],shoulder[j],top[j],top[i]],'#40b1df',(normal[0],normal[1],60))
    face(top,'#33a4d6',(0,0,1))
    box((-91,y-14,148.2),(70,y-11,148.8),'#8ad0e3')
    for x in [-95,95]:
        cylinder((x,y,148),(x,y,150),2.3,'#334c59','#8fabb1',12)

# Compact black chassis, lower skids and mounts.
for y in [-91,91]:
    box((-153,y-5,8),(153,y+5,15),'#3a535f')
    box((-138,y-4,31),(138,y+4,39),'#4c6772')
    box((-136,y-5,107),(136,y+5,115),'#354d5b')
    for x in [-126,126]:
        box((x-5,y-5,14),(x+5,y+5,114),'#3e5964')
        box((x-5,y+5,42),(x+5,y+6,95),'#657d81')
for x in [-126,0,126]:box((x-5,-92,31),(x+5,92,37),'#364c56')
for y in [-65,65]:float_module(y)

# Battery enclosure and the main cylindrical pressure housing.
cylinder((-105,0,37),(92,0,37),17,'#334e5e','#172d3b')
cylinder((-119,0,80),(113,0,80),31,'#7195a4','#34566b')
for x in [-103,73]:ring((x-4,0,80),(x+4,0,80),33,30,'#293e4a','#56747f')
# Small surface details communicate a separate electronics enclosure.
box((-78,6,106),(62,9,108),'#afc7c9')
box((-70,11,103),(51,14,105),'#547e8e')
cylinder((112,0,80),(128,0,80),32,'#233c4c','#526d79')
ring((128,0,80),(137,0,80),24,18,'#1d3445','#7a959d')
cylinder((132,0,80),(138,0,80),17,'#123344','#15566c')
cylinder((138,0,80),(139,0,80),9,'#10394f','#091f32')
cylinder((139,3,85),(140,3,85),3,'#bde9e3','#bde9e3',16)

# Four vectored horizontal thrusters and two vertical thrusters.
for x in [-106,106]:
    for y in [-112,112]:
        box((x-9,min(y,y*.8),72),(x+9,max(y,y*.8),81),'#314953')
        duct((x,y,79),(1 if x>0 else -1, .75 if y>0 else -.75, 0))
for x in [-70,70]:duct((x,0,126),(0,0,1),21,24)

# Camera lights sit on the front cross member.
for y in [-42,42]:
    cylinder((122,y,101),(142,y,101),7,'#304551','#728b8d',24)
    cylinder((142,y,101),(143,y,101),5,'#ead9ac','#e8dbad',24)

# A mounted arm has clear joints and a purposeful path to the gripper.
box((125,-23,34),(153,23,42),'#536a73')
arm=[(145,0,53),(192,0,96),(239,0,65),(270,0,44)]
for a,b in zip(arm,arm[1:]):
    cylinder(a,b,8,'#d9b574','#c6a162',24)
    # An outer cable runs along each link.
    cylinder(add(a,(0,8,0)),add(b,(0,8,0)),1.4,'#354b56',n=10)
for x,y,z in arm[:-1]:
    cylinder((x,-12,z),(x,12,z),13,'#344754','#a3b5b7',24)
    cylinder((x,12,z),(x,14,z),8,'#ad8b52','#d6b677',24)
    cylinder((x,14,z),(x,15,z),3,'#4b626d','#b9cdcc',12)
cylinder((266,0,47),(278,0,37),8,'#48626d','#2b4554',20)
for side in [-1,1]:
    pts=[(276,side*3,37),(286,side*14,30),(297,side*13,17),(292,side*7,13)]
    for a,b in zip(pts,pts[1:]):cylinder(a,b,2.8,'#a9c4c2',n=12)
# The small sample is illustrative, not a defined challenge object.
cylinder((293,0,3),(293,0,17),6,'#d1a46d','#edd0a4',20)
ring((293,0,15),(293,0,18),6.2,4.8,'#738b8b','#a5b9b1',20)

header='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" fill="none">
  <title>Conceptual compact underwater vehicle with a manipulator</title>
  <desc>A blue vehicle with buoyancy modules, an electronics enclosure, ducted thrusters and a mounted arm reaching for a small sample.</desc>
  <defs><radialGradient id="water"><stop stop-color="#477e83" stop-opacity=".14"/><stop offset="1" stop-color="#477e83" stop-opacity="0"/></radialGradient><filter id="soft-shadow" x="-30%" y="-100%" width="160%" height="300%"><feGaussianBlur stdDeviation="13"/></filter></defs>
  <ellipse cx="388" cy="311" rx="365" ry="260" fill="url(#water)"/>
  <ellipse cx="378" cy="458" rx="233" ry="44" fill="#021923" opacity=".38" filter="url(#soft-shadow)"/>
  <g stroke="#83b8b5" opacity=".09"><ellipse cx="395" cy="465" rx="300" ry="71"/><ellipse cx="395" cy="465" rx="340" ry="91"/></g>
  <g stroke-linejoin="round">'''
svg=header+'\n'+ '\n'.join('    '+element for _,element in sorted(faces,key=lambda f:f[0]))+'\n  </g>\n</svg>\n'
target=Path(__file__).resolve().parents[1]/'assets/images/challenge-uvms.svg'
target.write_text(svg,encoding='utf-8',newline='\n')
print(f'Wrote {target.name}: {len(faces)} visible surfaces.')
