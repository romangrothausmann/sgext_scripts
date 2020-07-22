#!/usr/bin/env python3

import sgext


def main():
    
    import sys       # to get command line args
    import argparse  # to parse options for us and print a nice help message

    argv = sys.argv

    if __file__ in argv:
        argv = argv[argv.index(__file__) + 1:]  # get all args after __file__

    usage_text =  "Skeletonize binary image with SGEXT:"
    usage_text +=  __file__ + " [options]"
    
    parser = argparse.ArgumentParser(description=usage_text)

    parser.add_argument("-i", "--input", dest="input", metavar='FILE', required=True, help="Input file name containing binary image for skeletonization")
    parser.add_argument("-o", "--output", dest="output", metavar='FILE', required=True, help="Output file name for saving the voxel skeleton")
 
    args = parser.parse_args()

    if not argv:
        parser.print_help()
        return

    if not args.input:
       print('Need an input file')
       parser.print_help()
       sys.exit(1)

    if not args.output:
       print('Need an output file')
       parser.print_help()
       sys.exit(1)

    # Thin Parameters
    skel_type="end"
    select_type="dmax"
    persistence=2
    verbose=True
    profile=True
       
    img = sgext.itk.read_as_binary(args.input)
    print('read input file')

    dmap_img = sgext.scripts.create_distance_map(img)
    print('dm created')
    thin_img = sgext.scripts.thin(input=img,
                                  skel_type=skel_type,
                                  select_type=select_type,
                                  input_distance_map_image=dmap_img,
                                  tables_folder=sgext.tables_folder,
                                  persistence=persistence,
                                  profile=profile,
                                  verbose=verbose)
    print('write output file')
    sgext.itk.write(thin_img, args.output)


if __name__ == "__main__":
    main()

