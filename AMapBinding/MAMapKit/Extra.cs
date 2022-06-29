using System;
using System.Collections.Generic;
using CoreLocation;

namespace MAMapKit {
    public partial class MAPolygon {
        public static unsafe MAPolygon PolygonWithCoordinates(CLLocationCoordinate2D[] coords, nuint count) {
            MAPolygon polygon = null;
            fixed (void* arrPtr = coords) {
                IntPtr ptr = new IntPtr(arrPtr);
                polygon = MAPolygon.PolygonWithCoordinates(ptr, count);
            }
            return polygon;
        }
    }

    public partial class MAMultiPoint {
        public unsafe MAMapPoint[] GetPoints() {
            var ptr = IntPtr.Zero;
            int count = (int)this.PointCount;
            var array = new List<MAMapPoint>();

            ptr = this.Points;
            unsafe {
                MAMapPoint* ptrPoint = (MAMapPoint*)ptr;
                for (int i = 0; i < count; i++) {
                    array.Add(*ptrPoint++);
                }
            }

            return array.ToArray();
        }
    }

}
