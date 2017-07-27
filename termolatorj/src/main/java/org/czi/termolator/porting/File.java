package org.czi.termolator.porting;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 *
 */
public class File<T> {

    public String name;

    public InternalStream stream;

    public File(String name) {
        this.name = name;
    }

    public InternalStream openText(String mode, String encoding, String errors) {

        if (stream == null)
            stream = new InternalStream(name);
        return stream;
    }

    public InternalStream openText(String mode) {
        return openText(mode, null, null);
    }

    public InternalStream openText() {

        return openText("r");
    }

    public List<String> readlines() {
      // @todo wrap lines in in File T is File;
      // @todo @hack for now
        assert stream != null;
        return stream.readlines();
    }
}


class InternalStream {

    private String name;
    private java.io.File file;

    InternalStream(String name)
    {

        this.name = name;
        this.file = new java.io.File(name);
    }

    public java.util.List<String> readlines() {
        // @todo wrap lines in in File T is File;
        // @todo @hack for now

        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader(file));

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

    public void write(String text) {
        FileWriter w = null;

        try {
            w = new FileWriter(file);
            w.write(text);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                w.close();
            }
            catch(IOException e) {}
        }
    }

    public Object __enter__(Object self) {
        return this;
    }

}
