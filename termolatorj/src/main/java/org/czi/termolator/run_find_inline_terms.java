package org.czi.termolator;

import jep.Jep;
import jep.JepConfig;
import jep.JepException;
import jep.python.PyModule;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

/**
 *
 */
public class run_find_inline_terms {

    private static final String root = "/development/projects/04_clients/czi/ds/The_Termolator/";

    public static void main(String[] args) throws JepException {

        File pwd = new File(".");
        JepConfig config = new JepConfig();
        config.addIncludePaths(new String[]{"."});

        Jep jep = new Jep(false, pwd.getAbsolutePath());
//        jep.eval("import py_compile");
//        jep.eval("py_compile.compile(file='build/testScript.py', cfile='build/testScript.pyc')");
//        jep.eval(null);
        jep.runScript(root + "run_find_inline_terms.py"); //DAVETEST.internal_prefix_list false
        Object result = null; //jep.getValue("isGood()");
        jep.close();
        if(!Boolean.TRUE.equals(result)){
            throw new IllegalStateException("isGood() returned " + result);
        }

    }
}
