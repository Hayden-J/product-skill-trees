// 저장소 안내서의 PNG를 다시 만드는 편집 가능한 소스 (macOS + Swift/AppKit).
// 저장소 루트에서 실행:
// swift -module-cache-path /private/tmp/product-flowchart-swift-cache docs/assets/render-flowcharts.swift docs/assets
// 과제 스킬의 필수 도구가 아니다. 다른 환경에서는 사용 가능한 도형 도구로 같은 내용을 그린다.
// docs/skill-map.md와 docs/development-handoff.md의 설명·텍스트·단계 표를 변경하면 함께 갱신한다.
import AppKit

let output = URL(fileURLWithPath: CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "docs/assets", isDirectory: true)
try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
let ink = NSColor(calibratedRed: 0.12, green: 0.18, blue: 0.27, alpha: 1)
let blue = NSColor(calibratedRed: 0.89, green: 0.94, blue: 1, alpha: 1)
let green = NSColor(calibratedRed: 0.88, green: 0.96, blue: 0.91, alpha: 1)
let gray = NSColor(calibratedWhite: 0.95, alpha: 1)

func text(_ value: String, _ rect: NSRect, size: CGFloat = 24, bold: Bool = false, align: NSTextAlignment = .center, background: Bool = false) {
    if background { NSColor.white.setFill(); rect.fill() }
    let style = NSMutableParagraphStyle(); style.alignment = align
    style.lineBreakMode = .byWordWrapping
    (value as NSString).draw(in: rect, withAttributes: [
        .font: bold ? NSFont.boldSystemFont(ofSize: size) : NSFont.systemFont(ofSize: size),
        .foregroundColor: ink, .paragraphStyle: style
    ])
}
func box(_ x: CGFloat, _ y: CGFloat, _ w: CGFloat, _ title: String, _ detail: String, color: NSColor = blue) {
    let rect = NSRect(x: x, y: y, width: w, height: 86)
    color.setFill(); let path = NSBezierPath(roundedRect: rect, xRadius: 14, yRadius: 14); path.fill()
    ink.withAlphaComponent(0.35).setStroke(); path.lineWidth = 1.5; path.stroke()
    text(title, NSRect(x: x+10, y: y+12, width: w-20, height: 32), size: 26, bold: true)
    text(detail, NSRect(x: x+10, y: y+49, width: w-20, height: 30), size: 21)
}
func arrow(_ points: [(CGFloat, CGFloat)], dashed: Bool = false) {
    guard points.count > 1 else { return }
    ink.setStroke(); ink.setFill()
    let path = NSBezierPath(); path.lineWidth = 2.5
    if dashed { path.setLineDash([8, 6], count: 2, phase: 0) }
    path.move(to: NSPoint(x: points[0].0, y: points[0].1))
    for p in points.dropFirst() { path.line(to: NSPoint(x: p.0, y: p.1)) }; path.stroke()
    let last=points[points.count-1], prev=points[points.count-2]
    let angle=atan2(last.1-prev.1,last.0-prev.0), len: CGFloat=13, spread: CGFloat=0.48
    let head=NSBezierPath();head.move(to:NSPoint(x:last.0,y:last.1))
    head.line(to:NSPoint(x:last.0-len*cos(angle-spread),y:last.1-len*sin(angle-spread)))
    head.line(to:NSPoint(x:last.0-len*cos(angle+spread),y:last.1-len*sin(angle+spread)))
    head.close();head.fill()
}
func label(_ value: String, _ x: CGFloat, _ y: CGFloat, _ w: CGFloat) {
    text(value, NSRect(x:x,y:y,width:w,height:31),size:19,background:true)
}
func render(_ name: String, width: CGFloat, height: CGFloat, draw: () -> Void) throws {
    // 명시적인 픽셀 크기: 실행 기기의 디스플레이 배율에 영향을 받지 않는다.
    guard let bitmap = NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:Int(width),pixelsHigh:Int(height),bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0),
          let context = NSGraphicsContext(bitmapImageRep:bitmap) else { fatalError("PNG context unavailable") }
    NSGraphicsContext.saveGraphicsState();NSGraphicsContext.current=context
    context.cgContext.translateBy(x:0,y:height);context.cgContext.scaleBy(x:1,y:-1)
    NSGraphicsContext.current=NSGraphicsContext(cgContext:context.cgContext,flipped:true)
    NSColor.white.setFill();NSRect(x:0,y:0,width:width,height:height).fill()
    draw();NSGraphicsContext.restoreGraphicsState()
    guard let data=bitmap.representation(using:.png,properties:[:]) else { fatalError("PNG encoding failed") }
    try data.write(to:output.appendingPathComponent(name))
    print("Generated \(name) (\(Int(width))×\(Int(height)))")
}

try render("skill-map-flow.png",width:1560,height:1500) {
    text("필요한 단계부터 시작하는 스킬 흐름",NSRect(x:50,y:25,width:1460,height:50),size:34,bold:true)
    // 연결을 먼저 그려 노드 경계 안으로 선이 들어가지 않게 한다.
    arrow([(550,143),(290,143),(290,235)])
    arrow([(750,186),(750,380)])
    arrow([(290,321),(290,380)])
    arrow([(480,423),(550,423)])
    arrow([(100,423),(45,423),(45,1293),(550,1293)])
    arrow([(950,423),(1030,423)])
    arrow([(1220,466),(1220,568),(950,568)])
    arrow([(750,466),(750,525)])
    arrow([(750,611),(750,670)])
    arrow([(550,713),(290,713),(290,815)])
    arrow([(750,756),(750,815)])
    arrow([(950,713),(1215,713),(1215,815)])
    arrow([(290,901),(290,1003),(325,1003)])
    arrow([(750,901),(750,960)])
    arrow([(625,1046),(625,1105)])
    arrow([(625,1191),(625,1250)])
    arrow([(1215,901),(1215,1198),(915,1198),(915,1250)])
    arrow([(950,1293),(1100,1293)])
    arrow([(750,1336),(750,1405),(1515,1405),(1515,690),(950,690)],dashed:true)
    box(550,100,400,"목적·제출물·제약·시간","요청 범위와 시작 단계 확인",color:gray)
    box(100,235,380,"인터뷰","실제 사례·근거")
    box(100,380,380,"문제 정의","원인·바꿀 지점")
    box(550,380,400,"요구 정리","조건·검증 기준")
    box(1030,380,380,"대안 평가","선택이 필요할 때만")
    box(550,525,400,"실제 선택·위임","기존 선택 유지 또는 새 선택")
    box(550,670,400,"현재 기준 문서","PLAN 또는 지정 문서",color:green)
    box(100,815,380,"UX 설계","화면·행동·상태·복구")
    box(550,815,400,"백엔드 설계","데이터·처리·저장·권한")
    box(1030,815,370,"산출물 작성","그 밖의 과제")
    box(325,960,600,"필요한 설계 통합","입출력·권한·실패 처리 대조")
    box(325,1105,600,"첫 흐름 구현","요청·위임된 범위")
    box(550,1250,400,"결과 검증","독립 기대값과 실제 결과 대조",color:green)
    box(1100,1250,330,"제출·본인 설명","요구된 결과·근거·한계",color:gray)
    label("근거·문제 확인 필요",200,180,240)
    label("문제·방식이 정해짐",760,265,245)
    label("해결안·구현 포함 →",300,470,230)
    label("문제 발굴까지만 요청",50,1170,260)
    label("기존 선택 유지",760,485,210)
    label("화면이 있는 제품",170,765,240)
    label("데이터·처리 필요",760,765,235)
    label("수정·현재 상태 반영 → 기준 문서",855,1370,430)
    text("모든 단계를 의무적으로 수행하지 않는다. 필요한 설계만 선택하며, 검증 후 현재 상태를 갱신한다.",NSRect(x:60,y:1450,width:1440,height:32),size:22)
}

try render("development-handoff-flow.png",width:1320,height:1050) {
    text("스킬 결과를 현재 기준 문서에 연결",NSRect(x:40,y:25,width:1240,height:50),size:34,bold:true)
    arrow([(660,186),(660,255)])
    arrow([(660,341),(660,440)])
    arrow([(360,483),(460,483)])
    arrow([(960,483),(860,483)])
    arrow([(660,526),(660,630)])
    arrow([(660,716),(660,810)])
    arrow([(460,853),(405,853),(405,540),(550,540),(550,526)],dashed:true)
    arrow([(800,526),(800,570),(1120,570),(1120,630)])
    box(460,100,400,"원문·응답·데이터","실제 입력과 출처",color:gray)
    box(460,255,400,"지금 필요한 스킬","요청된 범위만 수행")
    box(460,440,400,"현재 기준 문서","PLAN 또는 지정 문서",color:green)
    box(40,440,320,"Worklog","결정·변경 이유",color:gray)
    box(960,440,320,"상세 근거·실행 증거","필요한 경우에만 분리",color:gray)
    box(460,630,400,"첫 흐름 설계·구현","요구·선택·설계 적용")
    box(460,810,400,"기대값과 실제 결과 대조","실행 증거·한계·수정 필요",color:green)
    box(960,630,320,"제출 결과물","제출 양식에 맞춰 편집",color:gray)
    label("판단·요약 반영",670,375,220)
    label("결정 연결",250,395,175)
    label("요약·원본 링크",880,395,225)
    label("결과·현재 상태 갱신",90,765,295)
    text("PLAN: 현재 판단과 다음 행동   ·   Worklog: 결정 이력   ·   상세 자료: 근거 원본",NSRect(x:40,y:945,width:1240,height:35),size:24)
    text("한 스킬만 요청된 경우 별도 PLAN을 강제하지 않는다. 제출본 작성과 실제 제출은 구분한다.",NSRect(x:40,y:990,width:1240,height:35),size:22)
}
