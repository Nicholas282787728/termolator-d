package org.czi.termolator.porting;

import java.io.*;
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
            stream = new InternalStream(name, mode);
        if (mode != null && mode.contains("w")) {
            stream.empty();
        }
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
    private java.io.RandomAccessFile file;

    InternalStream(String name, String mode) {

        this.name = name;
        try {
            if (mode != null && mode.contains("w")) {
                mode = "r" + mode;
            }

            this.file = new RandomAccessFile(new java.io.File(name), mode);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    public java.util.List<String> readlines() {
        // @todo wrap lines in in File T is File;
        // @todo @hack for now

        try {
            file.seek(0);
            String line;
            List<String> lines = new ArrayList<String>();
            while ((line = file.readLine()) != null) {
                System.out.println("reading line " + line);
                lines.add(line);
            }

            return lines;

        } catch (IOException e) { e.printStackTrace(); return null; }
    }

    public void write(String text) {

        try {
            file.writeBytes(text);

        } catch (IOException e) { e.printStackTrace(); }
    }

    public Object __enter__(Object self) {
        return this;
    }

    public void empty() {
        try {
            System.out.println("Resetting file " + name);
            file.setLength(0);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
