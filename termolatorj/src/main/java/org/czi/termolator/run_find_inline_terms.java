package org.czi.termolator;

import jep.Jep;
import jep.JepConfig;
import jep.JepException;
import jep.python.PyModule;
import org.omg.CORBA.SystemException;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;

/**
 *
 */
public class run_find_inline_terms {

    private static final String root = "/development/projects/04_clients/czi/ds/The_Termolator/";
    private static final String NYU_DIR = "/development/projects/04_clients/czi/ds/The_Termolator/tests/czi/DAVETEST_small/source/";

    public static void main(String[] args)  {

        try {

            File pwd = new File(".");
            JepConfig config = new JepConfig();
            config.addIncludePaths(new String[]{".", root});

            //Jep jep = new Jep(false, pwd.getAbsolutePath());
            Jep jep = new Jep(config);
            jep.eval("import DataDef");
            jep.eval(null);

            jep.runScript(root + "run_find_inline_terms.py");

            jep.eval("dictionary.initialize_utilities()");

            jep.eval("find_inline_terms_for_file_list(File('DAVETEST.internal_prefix_list'), dict_prefix=False)");
            //jep.eval("main(['" + NYU_DIR +"DAVETEST.internal_prefix_list', False])");
            Object result = null; //jep.getValue("isGood()");
            jep.close();
//        if(!Boolean.TRUE.equals(result)){
//            throw new IllegalStateException("isGood() returned " + result);
//        }
        } catch(JepException e) {
            System.out.println("Error " + e);
        }
    }
}
