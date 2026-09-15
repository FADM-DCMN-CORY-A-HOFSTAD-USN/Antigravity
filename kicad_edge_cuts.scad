// =================================================================
// TYPE-S SAIYA - KICAD EDGE.CUTS GENERATOR
// Exports 2D DXF blueprints for PCB Fabrication matching the SCAD Steel.
// =================================================================
include <shocks.scad>;

// Dynamic parameters (can be injected by Python/Gantry)
board_width = 244;
board_length = 305;
mount_radius = 2; // Screw radius
clearance = 1.5;  // Extra clearance for the rubber shock bushings

module board_outline_2d() {
    // We use projection() to flatten the 3D logic into a strict 2D DXF for KiCad
    projection(cut = false) {
        difference() {
            // 1. The Main PCB Silhouette
            square([board_width, board_length], center=false);
            
            // 2. Subtract the Drill Holes (Scaled up to fit the rubber shock absorbers)
            // Using standard ATX mounting points as an example
            positions = [
                [6.35, 6.35], [6.35, 165], [6.35, 285],
                [165, 6.35], [165, 165], [165, 285],
                [238, 6.35], [238, 165], [238, 285]
            ];
            
            for (pos = positions) {
                translate([pos[0], pos[1], 0])
                    circle(r = mount_radius + clearance, $fn=50);
            }
        }
    }
}

// Execute
board_outline_2d();
