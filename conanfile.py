import os
from conans import ConanFile, CMake, tools

class CppCheckConan(ConanFile):
    name = "cppcheck_installer"
    version = "1.89"
    description = ("CppCheck is a linter for C++ that can catch various errors.")
    topics = ("Cpp Check", "static analyzer", "linter")
    url = "https://github.com/mjvk/conan-cppcheck_installer"
    homepage = "https://github.com/danmar/cppcheck/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "GPL-3.0-or-later"
    exports = ["LICENSE"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    
    settings = "compiler", "os_build", "arch_build"
    
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def source(self):
        sha256 = "37452d378825c7bd78116b4d7073df795fa732207d371ad5348287f811755783"
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        os.rename("cppcheck-%s" % self.version, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)
        self.copy("*", dst=os.path.join("bin","cfg"), src=os.path.join(self._source_subfolder,"cfg"))
        cmake = self._configure_cmake()
        cmake.install()

    def package_id(self):
        del self.info.settings.compiler

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info("Appending PATH environment variable: {}".format(bindir))
        self.env_info.PATH.append(bindir)