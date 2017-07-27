package org.czi.termolator.porting;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 *
 */
public class File2<T> {

    private String name;

    public File2(String name) {
        this.name = name;
    }

    public InternalStream openText(String mode, String encoding, String errors) {
        return new InternalStream(name);
    }

    public InternalStream openText(String mode) {
        return new InternalStream(name);
    }

    public Object doThis() {
        return null;
    }
}


class InternalStream {


    private String name;

    public InternalStream(String name)
    {
        this.name = name;
    }

    public java.util.List<String> readlines() {
        // @todo wrap lines in in File T is File;
        // @todo @hack for now
        java.io.File b = new java.io.File(name);

        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader(b));

            String line = null;
            // if no more lines the readLine() returns null
            List lines = new ArrayList<String>();
            while ((line = br.readLine()) != null) {
                // reading lines until the end of the file
                lines.add(line);
            }


            return lines;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        } finally {
            try {
                br.close();
            }
            catch(IOException e) {}
        }
    }

    public Object __enter__(Object self) {
        return this;
    }

}
