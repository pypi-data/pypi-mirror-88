from ._MadxMadxComparison import MADXVsMADX
try:
    from ._MadxTransportComparison import MADXVsTRANSPORT
except ImportError:
    print("No pytransport functionality")
