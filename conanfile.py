from conans import ConanFile, CMake, tools


class CorradeConan(ConanFile):
    name = "corrade"
    version = "2018.04"
    license = "MIT"
    url = "https://github.com/inexorgame/conan-corrade"
    description = "Utility library for C++ Plugins, tests and resources inlining utils"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/mosra/corrade --recursive -b v{}".format(self.version))
        tools.replace_in_file("corrade/CMakeLists.txt", "project(Corrade ${LANG})",
                              '''project(Corrade ${LANG})

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="corrade", definitions={
                        "BUILD_DEPRECATED": False,
                        "WITH_INTERCONNECT": False,
                        "BUILD_STATIC": False if self.shared else True})
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include/Corrade", src="corrade/src/Corrade")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["CorradeTestSuite", "CorradePluginManager", "CorradeUtility"]

