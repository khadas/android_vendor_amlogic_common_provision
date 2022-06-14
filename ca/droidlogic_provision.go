package droidlogic_provision

import (
     // "fmt"
     "android/soong/android"
     "android/soong/cc"
     "github.com/google/blueprint/proptools"
)

func init() {
     // fmt.Println("init: droidlogic_provision")
     android.RegisterModuleType("provision_go_defaults", provision_go_DefaultsFactory)
}

func provision_go_DefaultsFactory() (android.Module) {
    module := cc.DefaultsFactory()
    android.AddLoadHook(module, func(ctx android.LoadHookContext) {
         type props struct {
             Enabled *bool
         }
         p := &props{}
         p.Enabled = proptools.BoolPtr(true)

         if (ctx.Config().DeviceName() == "sabrina") {
             p.Enabled = proptools.BoolPtr(false)
             // fmt.Println("DeviceName is sabrina")
         }

         if (ctx.Config().DeviceName() == "boreal") {
             p.Enabled = proptools.BoolPtr(false)
             // fmt.Println("DeviceName is boreal")
         }

         ctx.AppendProperties(p)
    })
    return module
}
