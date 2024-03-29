import os
from conans import ConanFile, CMake, tools


class CppCheckConan(ConanFile):
    name = "cppcheck_installer"
    version = "1.88"
    url = "https://github.com/bincrafters/conan-protoc_installer"
    homepage = "https://github.com/danmar/cppcheck/"
    topics = ("Cpp Check", "static analyzer")
    author = "mjvk <>"
    description = ("flatc is a compiler for flatbuffers schema files. It can "
                   "generate among others C++, Java and Python code.")
    license = "BSD-3-Clause"
    exports = ["LICENSE.txt"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "compiler", "arch", "os_build", "arch_build"
    #short_paths = True
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def source(self):
        sha256 = "4aace0420d6aaa900b84b3329c5173c2294e251d2e24d8cba6e38254333dde3f"
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        os.rename("cppcheck-%s" % self.version, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["FLATBUFFERS_BUILD_TESTS"] = False
        cmake.definitions["FLATBUFFERS_BUILD_FLATLIB"] = False
        cmake.definitions["FLATBUFFERS_BUILD_FLATHASH"] = False
        cmake.definitions["FLATBUFFERS_INSTALL"] = True
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy("*", dst=os.path.join("bin","cfg"), src=os.path.join(self._source_subfolder,"cfg"))
        cmake = self._configure_cmake()
        cmake.install()

    def package_id(self):
        del self.info.settings.compiler
        del self.info.settings.arch
        self.info.include_build_settings()

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))