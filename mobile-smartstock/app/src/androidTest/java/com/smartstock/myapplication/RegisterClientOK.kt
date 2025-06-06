package com.smartstock.myapplication


import android.content.res.Resources
import android.view.View
import android.view.ViewGroup
import androidx.test.espresso.Espresso.onData
import androidx.test.espresso.Espresso.onView
import androidx.test.espresso.Espresso.pressBack
import androidx.test.espresso.UiController
import androidx.test.espresso.ViewAction
import androidx.test.espresso.action.ViewActions.*
import androidx.test.espresso.assertion.ViewAssertions.*
import androidx.test.espresso.matcher.RootMatchers
import androidx.test.espresso.matcher.RootMatchers.isPlatformPopup
import androidx.test.espresso.matcher.ViewMatchers.*
import androidx.test.ext.junit.rules.ActivityScenarioRule
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.LargeTest
import com.smartstock.myapplication.Utils.getLocalizedText
import org.hamcrest.Description
import org.hamcrest.Matcher
import org.hamcrest.Matchers.allOf
import org.hamcrest.Matchers.anything
import org.hamcrest.Matchers.`is`
import org.hamcrest.TypeSafeMatcher
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@LargeTest
@RunWith(AndroidJUnit4::class)
class RegisterClientOK {

    @Rule
    @JvmField
    var mActivityScenarioRule = ActivityScenarioRule(SplashActivity::class.java)

    fun waitFor(millis: Long): ViewAction {
        return object : ViewAction {
            override fun getConstraints(): Matcher<View> = isRoot()

            override fun getDescription(): String = "Wait for $millis milliseconds."

            override fun perform(uiController: UiController, view: View?) {
                uiController.loopMainThreadForAtLeast(millis)
            }
        }
    }

    @Test
    fun registerClientOK() {
        onView(isRoot()).perform(waitFor(4000))
        val textInputEditText = onView(withId(R.id.email))
            .perform(replaceText("camilo@sta.com"), closeSoftKeyboard())

        val textInputEditText2 = onView(withId(R.id.password))
            .perform(replaceText("1234567"), closeSoftKeyboard())

        val materialButton = onView(withId(R.id.buttonLogin))
            .perform(click())

        onView(isRoot()).perform(waitFor(5000))
        val bottomNavigationItemView = onView(
            withId(R.id.nav_menu)
        )
        bottomNavigationItemView.perform(click())
        onView(isRoot()).perform(waitFor(1000))


        val materialTextView = onView(
            allOf(
                withId(android.R.id.title), withText(getLocalizedText("Menu Create Client")),
                childAtPosition(
                    childAtPosition(
                        withId(android.R.id.content),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        materialTextView.perform(click())
        onView(isRoot()).perform(waitFor(1000))
        val textInputEditText3 = onView(
            allOf(
                withId(R.id.name),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.textField4_1),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        textInputEditText3.perform(replaceText("prueba"), closeSoftKeyboard())

        val textInputEditText4 = onView(
            allOf(
                withId(R.id.address),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.textField4_2),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        textInputEditText4.perform(replaceText("AVENIDA 100"), closeSoftKeyboard())
        onView(isRoot()).perform(waitFor(100))

        val textInputEditText5 = onView(
            allOf(
                withId(R.id.phone),
                childAtPosition(
                    childAtPosition(
                        withId(R.id.textField4_3),
                        0
                    ),
                    0
                ),
                isDisplayed()
            )
        )
        textInputEditText5.perform(replaceText("+573000000712"), closeSoftKeyboard())

        val textInputEditText6 = onView(withId(R.id.email_create_client))
            .perform(replaceText("prueba712@gmail.com"), closeSoftKeyboard())


        onView(isRoot()).perform(waitFor(100))

        onView(withId(R.id.textField4_5))
            .perform(click())

        onView(isRoot()).perform(waitFor(100))

        // Click the first item in the dropdown
        onView(withText(getLocalizedText("client_type_supermarket"))) // Replace with actual string shown in the list
            .inRoot(isPlatformPopup()) // This tells Espresso to look in the dropdown popup
            .perform(click())




        onView(withId(R.id.textField4_6))
            .perform(click())
        onView(isRoot()).perform(waitFor(100))
        // Click the first item in the dropdown
        onView(withText(getLocalizedText("zone_south"))) // Replace with actual string shown in the list
            .inRoot(isPlatformPopup()) // This tells Espresso to look in the dropdown popup
            .perform(click())

        onView(isRoot()).perform(waitFor(1000))
        onView(withId(R.id.buttonAcceptCreate))
            .check(matches(isDisplayed()))
            .check(matches(isEnabled()))
            .perform(click())

        onView(isRoot()).perform(waitFor(3000))


        val textViewPPal = onView(withId(R.id.client_list))
        textViewPPal.check(matches(withText(getLocalizedText("lista_de_clientes"))))
    }

    private fun childAtPosition(
        parentMatcher: Matcher<View>, position: Int
    ): Matcher<View> {

        return object : TypeSafeMatcher<View>() {
            override fun describeTo(description: Description) {
                description.appendText("Child at position $position in parent ")
                parentMatcher.describeTo(description)
            }

            public override fun matchesSafely(view: View): Boolean {
                val parent = view.parent
                return parent is ViewGroup && parentMatcher.matches(parent)
                        && view == parent.getChildAt(position)
            }
        }
    }
}
