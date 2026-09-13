// Gundam Robotics Systems
// Project: Type-S (Saiya) Anti-Gravity Platform
// Component: Initial Reactor Bed & Electromagnetic Coil Mounts (Legacy/Research)

// --- Global Parameters ---
bed_radius = 150;
bed_thickness = 20;
core_cutout_radius = 45;

coil_count = 8;               // Octagonal array for EM research
coil_mount_radius = 20;
coil_mount_height = 50;
flange_extension = 8;         // Lip to hold the copper windings in place

// --- Modules ---

module reactor_bed() {
    // The main heavy-duty mounting plate
    difference() {
        // Main Disc
        cylinder(r=bed_radius, h=bed_thickness, $fn=120);
        
        // Center Cavity (For core insertion or alignment)
        translate([0, 0, -1]) 
        cylinder(r=core_cutout_radius, h=bed_thickness + 2, $fn=100);
        
        // Radial Cooling / Wiring Slots
        for(i = [0 : 360/12 : 359]) {
            rotate([0, 0, i]) 
            translate([bed_radius * 0.55, 0, -1]) 
            hull() {
                cylinder(r=10, h=bed_thickness + 2, $fn=30);
                translate([25, 0, 0]) cylinder(r=10, h=bed_thickness + 2, $fn=30);
            }
        }
        
        // Mounting holes for the coil spools
        for(i = [0 : 360/coil_count : 359]) {
            rotate([0, 0, i]) 
            translate([bed_radius - 35, 0, -1]) 
            cylinder(r=5, h=bed_thickness + 2, $fn=30);
        }
    }
}

module coil_mount() {
    // Flanged spool to hold the electromagnetic copper windings
    difference() {
        union() {
            // Main Spool Body
            cylinder(r=coil_mount_radius, h=coil_mount_height, $fn=60);
            
            // Bottom Flange
            cylinder(r=coil_mount_radius + flange_extension, h=5, $fn=60);
            
            // Top Flange
            translate([0, 0, coil_mount_height - 5]) 
            cylinder(r=coil_mount_radius + flange_extension, h=5, $fn=60);
        }
        
        // Hollow core for cooling or ferrite rod insertion
        translate([0, 0, -1]) 
        cylinder(r=coil_mount_radius - 8, h=coil_mount_height + 2, $fn=60);
    }
}

// --- Assembly Render ---

// 1. The Main Reactor Bed
color("darkslategray") 
reactor_bed();

// 2. The Electromagnetic Coil Mounts
// Arranged in a radial array along the outer edge of the bed
for(i = [0 : 360/coil_count : 359]) {
    rotate([0, 0, i])
    translate([bed_radius - 35, 0, bed_thickness])
    color("copper") 
    coil_mount();
}

// --- Text Label ---
color("white")
translate([0, -bed_radius + 15, bed_thickness])
linear_extrude(2)
text("EM RESEARCH BED v1", size=8, halign="center", valign="center");
