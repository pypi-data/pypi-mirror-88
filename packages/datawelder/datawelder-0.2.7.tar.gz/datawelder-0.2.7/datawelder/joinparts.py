"""Join a single partition number across multiple data frames."""
import sys

import datawelder.join

partnum = int(sys.argv[1])
frame_paths = sys.argv[2:]

datawelder.join.join_partitions(
    partnum,
    frame_paths,
    None,
    output_format='json',
)
