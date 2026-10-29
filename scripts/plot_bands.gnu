
set terminal pngcairo size 1000,700
set output 'aln_bands_all.png'
set xlabel 'k-path'
set ylabel 'E - E_F (eV)'
set yrange [-20:15]
set xrange [0:*]
set title 'AlN Band Structure (PBE)'
plot for [i=2:31] 'aln_bands_multicol.dat' using 1:(column(i) - 8.5431) with lines linewidth 1.0 notitle
