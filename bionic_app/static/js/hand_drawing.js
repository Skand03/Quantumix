// Enhanced hand drawing with accurate finger bending
function drawFingerWithJoints(ctx, baseX, baseY, segments, extended, fingerName) {
    ctx.fillStyle = '#FFD1A4';
    ctx.strokeStyle = '#8B4513';
    ctx.lineWidth = 3;
    
    ctx.save();
    ctx.translate(baseX, baseY);
    
    let currentY = 0;
    const segmentLengths = segments.lengths;
    const segmentWidths = segments.widths;
    
    // Calculate curl angles for each segment
    const curlAngles = extended ? [0, 0, 0] : segments.curlAngles;
    
    for (let i = 0; i < segmentLengths.length; i++) {
        ctx.save();
        ctx.translate(0, currentY);
        
        // Rotate at joint
        if (i > 0) {
            ctx.rotate(curlAngles[i]);
        }
        
        // Draw segment
        const width = segmentWidths[i];
        const length = segmentLengths[i];
        
        ctx.beginPath();
        ctx.roundRect(-width/2, 0, width, length, 8);
        ctx.fill();
        ctx.stroke();
        
        // Draw joint knuckle
        if (i > 0) {
            ctx.fillStyle = '#D2A679';
            ctx.beginPath();
            ctx.arc(0, 0, width/2 + 2, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();
            ctx.fillStyle = '#FFD1A4';
        }
        
        // Draw fingernail on last segment
        if (i === segmentLengths.length - 1) {
            ctx.fillStyle = '#FFE5CC';
            ctx.beginPath();
            ctx.ellipse(0, length - 5, width * 0.4, width * 0.25, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();
        }
        
        currentY = length;
        ctx.restore();
        
        // Move to end of segment for next one
        ctx.translate(0, length * Math.cos(curlAngles[i]));
    }
    
    ctx.restore();
}
