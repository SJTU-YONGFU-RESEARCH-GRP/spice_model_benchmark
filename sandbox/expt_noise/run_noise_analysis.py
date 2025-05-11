#!/usr/bin/env python3
"""
Main script to run the noise analysis simulation and generate a report.
"""

import os
import sys
import argparse
from src.logger import Logger
from src.noise_analyzer import NoiseAnalyzer

def main():
    """
    Main function to parse arguments and run the noise analysis
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run noise analysis on SPICE models")
    parser.add_argument("--spice-file", default="noise_analysis.cir", 
                        help="Path to the SPICE netlist file (default: noise_analysis.cir)")
    parser.add_argument("--output-dir", default="results",
                        help="Directory for storing results (default: results)")
    parser.add_argument("--spice-cmd", default="ngspice",
                        help="Command to run SPICE simulator (default: ngspice)")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Logging level (default: INFO)")
    
    args = parser.parse_args()
    
    # Check if SPICE file exists
    if not os.path.exists(args.spice_file):
        print(f"Error: SPICE file '{args.spice_file}' not found.")
        return 1
    
    # Initialize and run analyzer
    try:
        analyzer = NoiseAnalyzer(
            spice_file=args.spice_file,
            output_dir=args.output_dir,
            log_level=args.log_level,
            spice_cmd=args.spice_cmd
        )
        
        result = analyzer.run_analysis()
        
        if result["status"] == "success":
            print(f"Analysis completed successfully. Report generated at {result['report_path']}")
            return 0
        else:
            print(f"Analysis failed: {result.get('message', 'Unknown error')}")
            return 1
    
    except Exception as e:
        print(f"Error running analysis: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 